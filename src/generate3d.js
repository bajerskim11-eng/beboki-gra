export async function generateHanys3D(file) {
  const image = await fileToDataUrl(file);
  const response = await fetch('/api/generate-3d', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image, prompt: 'detailed Polish bebok Hanys, full body, preserve exact reference design, premium stylized game-ready 3D character, detailed face, hair and clothing, clean silhouette' })
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || '3D generation failed');
  const b64 = data?.artifacts?.[0]?.base64 || data?.artifact?.base64;
  if (!b64) throw new Error('NVIDIA returned no GLB artifact');
  return Uint8Array.from(atob(b64), c => c.charCodeAt(0));
}
function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = reject; reader.readAsDataURL(file);
  });
}
