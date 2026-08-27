# Beboki Video Engine

Pierwszy backend generowania scen Beboków przez ComfyUI + Wan 2.1 I2V.

## Architektura

Shopify -> Beboki Video API -> ComfyUI -> Wan 2.1 I2V -> MP4

Postać jest wybierana z `characters.json`. Backend pobiera jej kanoniczną referencję z Shopify CDN, wysyła ją do ComfyUI przez `/upload/image`, a następnie uruchamia workflow Wan przez `/prompt`.

## Aktualne postacie

- Hanys — zielony, górnik, kilof
- Hopla — różowa, zwiadowczyni, plecak i hełm
- Fachura — niebieski, górnik, dwa świecące kilofy
- Podciep — szaro-fioletowy, latarnik, stara lampa

## Model

Pierwszy silnik używa `wan2.1_i2v_480p_14B_fp16.safetensors`.

Wymagane pliki:

- `ComfyUI/models/diffusion_models/wan2.1_i2v_480p_14B_fp16.safetensors`
- `ComfyUI/models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors`
- `ComfyUI/models/vae/wan_2.1_vae.safetensors`
- `ComfyUI/models/clip_vision/clip_vision_h.safetensors`

## Uruchomienie GPU

Na maszynie z NVIDIA GPU uruchom:

```bash
cd video-engine
bash scripts/setup_comfyui_wan21.sh
```

Skrypt pobiera ComfyUI i wymagane zasoby Wan z repozytorium `Comfy-Org/Wan_2.1_ComfyUI_repackaged`. Nie przechowujemy ciężkich modeli w GitHubie.

Można też użyć przygotowanego obrazu CUDA:

```bash
cd video-engine
docker compose -f docker-compose.gpu.yml up --build
```

Backend API będzie na porcie `8080`, a ComfyUI na `8188`.

## Backend

```bash
cd video-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export COMFYUI_URL=http://127.0.0.1:8188
uvicorn server:app --host 0.0.0.0 --port 8080
```

Sprawdzenie:

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/characters
```

## Pierwsza scena

```bash
curl -X POST http://127.0.0.1:8080/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "character_id": "fachura",
    "scene_prompt": "Fachura nocą schodzi pod Spodek. Słyszy dziwny dźwięk, odgarnia kamienie dwoma świecącymi niebieskimi kilofami i znajduje starą magiczną skrzynię.",
    "width": 512,
    "height": 512,
    "frames": 33
  }'
```

Backend zwróci `prompt_id`. Wynik sprawdzamy:

```bash
curl http://127.0.0.1:8080/jobs/<PROMPT_ID>
```

## Ciągłość postaci

`characters.json` jest źródłem prawdy dla wyglądu. Backend automatycznie dodaje blokadę tożsamości oraz negatywny prompt przeciw zmianie twarzy, futra, fryzury, ubioru i przedmiotów charakterystycznych.

To jest pierwszy poziom continuity. Następny etap to referencyjne adaptery/LoRA i pamięć między ujęciami, a potem generowanie całego odcinka z planem scen.

## Ważne

Wan 2.1 jest projektem open-source, ale generowanie 14B wymaga mocnego GPU. Nie będziemy próbować renderować tego na Twoim Macu. Mac będzie mógł obsługiwać Shopify i panel sterowania, a GPU będzie osobnym workerem.

## Następny etap

1. Uruchamiamy pierwszy render Fachury.
2. Dodajemy VACE/reference-to-video dla mocniejszej kontroli wyglądu.
3. Dodajemy Character LoRA/adapter dla każdego Beboka.
4. Dodajemy pamięć stanu między ujęciami.
5. Story Engine dzieli historię na sceny.
6. Pipeline automatycznie montuje odcinek.
7. Podpinamy `create episode` do Shopify.
