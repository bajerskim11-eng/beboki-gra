# Beboki Video Engine

Pierwszy backend generowania scen Beboków przez ComfyUI + Wan 2.1 I2V.

## Architektura

Shopify -> Beboki Video API -> ComfyUI -> Wan 2.1 I2V -> MP4

Postać jest wybierana z `characters.json`. Backend pobiera jej kanoniczną referencję z Shopify CDN, wysyła ją do ComfyUI przez `/upload/image`, a następnie uruchamia natywny workflow Wan przez `/prompt`.

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

ComfyUI ma natywne workflow dla Wan 2.1 I2V. Model 14B daje nam jakość potrzebną do pierwszych testów postaci; później dodamy lżejszy wariant dla tańszego renderowania.

## Uruchomienie

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

`characters.json` jest źródłem prawdy dla wyglądu. Backend automatycznie dodaje do promptu blokadę tożsamości oraz negatywny prompt przeciw zmianie twarzy, futra, fryzury, ubioru i przedmiotów charakterystycznych.

To jest pierwszy poziom continuity. Następny etap to referencyjne adaptery/LoRA i pamięć między ujęciami, a potem generowanie całego odcinka z planem scen.

## GPU

Model i ComfyUI są open-source, ale samo generowanie wymaga odpowiedniego GPU. Backend jest przygotowany tak, aby ComfyUI działało na osobnym serwerze GPU; Mac nie musi wykonywać generowania lokalnie.

## Następny etap

Po uruchomieniu pierwszego renderu dokładamy:

1. Character LoRA/adapter dla każdego Beboka.
2. pamięć stanu między ujęciami,
3. Story Engine dzielący historię na sceny,
4. automatyczny montaż odcinka,
5. endpoint Shopify `create episode`.
