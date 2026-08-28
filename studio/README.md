# Beboki Story Studio

Local-first studio do produkcji całej bajki „Beboki i Serce Śląska”.

## Co robi

- **Story Bible + pamięć**: zapisuje kanon świata, postaci, odcinki, sceny i decyzje.
- **Generator historii**: opcjonalnie używa Ollama do pisania scen, dialogów i promptów.
- **Generator grafik**: wysyła zadania do lokalnego ComfyUI.
- **Generator wideo**: wysyła zadania do ComfyUI z Wan2.1 / LTX-2.
- **Montaż**: FFmpeg składa wygenerowane klipy w MP4.
- **YouTube-ready**: docelowo 1920×1080, 24/25 fps, H.264/AAC.

## Open-source stack

- ComfyUI — silnik workflow dla obrazu/wideo.
- Qwen-Image / Qwen-Image-Edit — grafiki i zachowanie wyglądu postaci.
- Wan2.1 — image-to-video / text-to-video.
- Ollama — lokalny model językowy do scenariusza.
- SQLite — prosta lokalna pamięć projektu.
- FFmpeg — montaż i konwersja.
- Remotion — opcjonalna warstwa animowanych napisów/komiksowych przejść.

Kod/model to jedno; **GPU/energia nie są automatycznie darmowe**. Najlepiej uruchamiać generację na NVIDIA GPU albo w środowisku GPU/Colab.

## Start

```bash
cd studio
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload --port 8787
```

Otwórz `http://localhost:8787`.

### Ollama

Zainstaluj Ollama i pobierz dowolny lokalny model tekstowy, np. Qwen/Gemma zgodny z Twoją kartą:

```bash
ollama run qwen3
```

### ComfyUI

Uruchom ComfyUI i ustaw:

```env
COMFY_URL=http://127.0.0.1:8188
```

W ComfyUI przygotuj workflow API dla obrazu, image-to-video (Wan2.1) i ewentualnie LTX-2. Workflow JSON-y trzymaj w `studio/workflows/`.

## Zasada kanonu

Cztery dostarczone przez Ciebie Beboki są **referencją kanoniczną**. Studio przechowuje ich opisy w `story/canon.json`. Każdy prompt sceny automatycznie dołącza opis kanonu.

## Licencje

Sprawdź osobno licencję każdego modelu i assetu przed publikacją komercyjną. Qwen-Image i Wan2.1 deklarują Apache-2.0 dla swoich modeli; ComfyUI ma własną licencję. Nie zakładamy, że każdy pobrany checkpoint lub LoRA ma tę samą licencję.