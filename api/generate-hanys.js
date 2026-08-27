export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const apiKey = process.env.NVIDIA_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'NVIDIA_API_KEY is not configured.' });

  try {
    const { image } = req.body || {};
    if (!image || typeof image !== 'string' || !image.startsWith('data:image/')) {
      return res.status(400).json({ error: 'Send an image as a data:image/... base64 string.' });
    }

    const response = await fetch('https://ai.api.nvidia.com/v1/genai/microsoft/trellis', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify({
        mode: 'image',
        image,
        seed: 0,
        ss_sampling_steps: 25,
        slat_sampling_steps: 25
      })
    });

    const data = await response.json();
    if (!response.ok) return res.status(response.status).json({ error: data?.error || data });

    const artifact = data?.artifacts?.[0];
    if (!artifact?.base64) return res.status(502).json({ error: 'TRELLIS returned no GLB artifact.', response: data });

    return res.status(200).json({ glb: artifact.base64, mime: 'model/gltf-binary' });
  } catch (error) {
    return res.status(500).json({ error: 'Server error while contacting NVIDIA TRELLIS.' });
  }
}
