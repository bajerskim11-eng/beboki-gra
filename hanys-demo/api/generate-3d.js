const NVIDIA_URL = 'https://ai.api.nvidia.com/v1/genai/microsoft/trellis';
const ASSETS_URL = 'https://api.nvcf.nvidia.com/v2/nvcf/assets';

export const config = { maxDuration: 300 };

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  try {
    const key = process.env.NVIDIA_API_KEY;
    if (!key) return res.status(500).json({ error: 'Brak NVIDIA_API_KEY w Vercel Environment Variables.' });

    const { image, prompt = 'cute detailed Polish bebok character, full body, preserve the exact reference character design, premium stylized game-ready 3D character, detailed face and clothing, clean silhouette' } = req.body || {};
    if (!image || typeof image !== 'string' || !image.startsWith('data:image/')) {
      return res.status(400).json({ error: 'image is required as a data URL' });
    }

    const match = image.match(/^data:(image\/(?:png|jpeg|jpg));base64,(.+)$/);
    if (!match) return res.status(400).json({ error: 'Only PNG/JPEG images are supported.' });

    const contentType = match[1] === 'image/jpg' ? 'image/jpeg' : match[1];
    const bytes = Buffer.from(match[2], 'base64');

    // NVIDIA's hosted TRELLIS preview does not accept arbitrary inline images;
    // custom images must be staged through NVCF Assets and referenced by asset ID.
    const assetResponse = await fetch(ASSETS_URL, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
        Accept: 'application/json'
      },
      body: JSON.stringify({ contentType, description: 'Hanys reference image' })
    });

    const assetText = await assetResponse.text();
    if (!assetResponse.ok) {
      return res.status(assetResponse.status).send(assetText);
    }

    const asset = JSON.parse(assetText);
    if (!asset.assetId || !asset.uploadUrl) {
      return res.status(502).json({ error: 'NVIDIA asset service returned no upload URL.', details: asset });
    }

    const uploadResponse = await fetch(asset.uploadUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': contentType,
        'x-amz-meta-nvcf-asset-description': 'Hanys reference image'
      },
      body: bytes
    });

    if (!uploadResponse.ok) {
      const uploadText = await uploadResponse.text();
      return res.status(502).json({ error: 'Nie udało się wysłać obrazu do NVIDIA Asset Storage.', details: uploadText });
    }

    const nvidiaResponse = await fetch(NVIDIA_URL, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'NVCF-INPUT-ASSET-REFERENCES': asset.assetId
      },
      body: JSON.stringify({
        mode: 'image',
        image: `data:${contentType};asset_id,${asset.assetId}`,
        prompt: prompt.slice(0, 77),
        output_format: 'glb',
        samples: 1,
        seed: 0,
        no_texture: false,
        slat_cfg_scale: 7.5,
        ss_cfg_scale: 7.5,
        slat_sampling_steps: 50,
        ss_sampling_steps: 50
      })
    });

    const text = await nvidiaResponse.text();
    if (!nvidiaResponse.ok) return res.status(nvidiaResponse.status).send(text);

    let data;
    try { data = JSON.parse(text); } catch { data = { raw: text }; }
    return res.status(200).json({ ...data, assetId: asset.assetId });
  } catch (error) {
    console.error('Hanys 3D generation error:', error);
    return res.status(500).json({ error: error?.message || 'NVIDIA request failed' });
  }
}
