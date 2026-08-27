export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.NVIDIA_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'NVIDIA_API_KEY is not configured on the server.' });
  }

  try {
    const { messages } = req.body || {};
    if (!Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ error: 'messages must be a non-empty array.' });
    }

    const system = {
      role: 'system',
      content:
        'Jesteś AI przewodnikiem świata Beboków z Katowic. Odpowiadaj po polsku, ciekawie i naturalnie. Pomagaj użytkownikowi odkrywać Beboki, tworzyć questy, zagadki i historie. Nie udawaj, że znasz fakty, których nie podano.'
    };

    const response = await fetch('https://integrate.api.nvidia.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'openai/gpt-oss-20b',
        messages: [system, ...messages],
        temperature: 0.7,
        top_p: 0.9,
        max_tokens: 1024,
        stream: false
      })
    });

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error || 'NVIDIA API request failed.'
      });
    }

    return res.status(200).json({
      message: data.choices?.[0]?.message?.content || ''
    });
  } catch (error) {
    return res.status(500).json({ error: 'Server error while contacting NVIDIA NIM.' });
  }
}
