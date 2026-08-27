function getDataUrl(input) {
  if (typeof input !== 'string' || !input.startsWith('data:image/')) return null;
  if (input.length > 12_000_000) return null;
  return input;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const apiKey = process.env.NVIDIA_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'NVIDIA_API_KEY is not configured in Vercel.' });
  }

  try {
    const { image, personality = 'figlarny', profession = 'bebok z Katowic' } = req.body || {};
    const imageData = getDataUrl(image);

    if (!imageData) {
      return res.status(400).json({ error: 'Send a JPG/PNG image as a data:image/... base64 string.' });
    }

    const prompt = [
      'Transform the person in the reference photo into an original, friendly Katowice Bebok character sticker.',
      'Keep the person clearly recognizable: preserve their face shape, hairstyle, approximate age, expression and distinctive visual traits.',
      'Do not copy any existing copyrighted character. Create a new original Bebok design.',
      `Personality: ${personality}.`,
      `Role: ${profession}.`,
      'Use a charming hand-painted 3D animated game aesthetic, rounded slightly mischievous creature proportions, expressive eyes, detailed clothing and playful Polish/Silesian character.',
      'Full body, centered, facing camera, clean studio composition, simple warm neutral background, strong silhouette, polished collectible character art.',
      'No text, no logos, no watermark, no extra people, no distorted hands, no duplicate limbs.'
    ].join(' ');

    const response = await fetch('https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify({
        mode: 'Image Editing',
        prompt,
        image: [imageData],
        width: 1024,
        height: 1024,
        samples: 1,
        seed: 0,
        steps: 4
      })
    });

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({ error: data?.error || data?.detail || data });
    }

    const artifact = data?.artifacts?.[0];
    if (!artifact?.base64) {
      return res.status(502).json({ error: 'NVIDIA returned no image artifact.' });
    }

    return res.status(200).json({
      image: `data:image/png;base64,${artifact.base64}`,
      mime: 'image/png'
    });
  } catch (error) {
    console.error('Bebok generation error:', error);
    return res.status(500).json({ error: 'Server error while generating the Bebok.' });
  }
}
