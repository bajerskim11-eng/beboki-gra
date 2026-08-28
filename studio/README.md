# Beboki Story Studio

Local-first studio do produkcji całej bajki **„Beboki i Serce Śląska”**.

## Pipeline

`story bible → scene plan → keyframes → image-to-video → voice/music → FFmpeg → episode.mp4`

GitHub przechowuje kod, prompty i pamięć. Duże checkpointy modeli uruchamiamy na NVIDIA GPU / Colab / innym środowisku GPU — nie commitujemy wag ani sekretów.

## Open-source stack

- **ComfyUI** — orkiestracja workflowów obrazu i wideo.
- **Qwen-Image** — keyframe'y, komiksowe kadry i edycja obrazów.
- **Wan2.1 1.3B** — pierwszy test image-to-video przy małym VRAM.
- **Wan2.2 TI2V-5B** — docelowy upgrade do 720p image+text-to-video przy odpowiednim GPU.
- **Ollama** — lokalny scenarzysta/prompt planner.
- **SQLite** — trwała pamięć historii.
- **FFmpeg** — montaż odcinka.
- **Remotion** — opcjonalnie napisy i komiksowe przejścia.

## GPU setup

Uruchom `studio/scripts/bootstrap_gpu.sh` na Linux/NVIDIA/Colab-style runtime. Skrypt instaluje ComfyUI obok repo i tworzy katalogi modeli. Następnie `studio/scripts/run_comfy.sh` uruchamia ComfyUI.

## NVIDIA API

Możemy użyć NVIDIA NIM/API jako alternatywy dla lokalnego GPU. Klucz trzymaj wyłącznie jako zmienną środowiskową (`NVIDIA_API_KEY`) lub sekret środowiska. Nigdy nie zapisuj go w GitHub.

## Pierwszy odcinek

**Odcinek 1 — Co wyczuł pies?**

Noc w Katowicach. Pies nagle wyczuwa coś pod starą ceglaną kamienicą. Cztery Beboki ruszają za jego tropem. W piwnicy odkrywają pierwszy ślad prowadzący do fragmentu Serca Śląska.

Styl: filmowy, baśniowy Śląsk, mokry bruk, cegła, stare szyby i kopalniane konstrukcje, ciepłe latarnie, mgła, światło magiczne, komiksowe kadrowanie, spójna twarz/futro/ubiór kanonicznych Beboków.

## Docelowa historia

Psy wyczuwają ukryte fragmenty Serca Śląska. Beboki pomagają psom i wspólnie odnajdują kolejne fragmenty. Po złożeniu całego Serca następuje magiczna przemiana świata: powstaje utopijny, samowystarczalny Śląsk, w którym automatyzacja usuwa ciężką pracę, energia jest czysta i tania, a ludzie mają czas na życie, twórczość i pomaganie. Beboki otrzymują własną krainę „mlekiem i miodem płynącą”.

## Ważne

Nie deklarujemy „działa”, dopóki nie wykonamy testu generacji na GPU. Darmowy kod/model nie oznacza darmowej mocy obliczeniowej. Licencję każdego modelu, LoRA i assetu sprawdzamy osobno przed publikacją komercyjną.
