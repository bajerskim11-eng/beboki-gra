# Beboki Video Engine

Cel: generowanie spójnych filmów z tymi samymi postaciami Beboków.

## Architektura

Shopify (frontend) -> Beboki API -> Story Engine -> ComfyUI -> video model -> storage/CDN -> Shopify

### Postać jest stałym zasobem

Każdy Bebok ma:
- `id`
- referencyjny obraz
- opis wyglądu
- ubranie i przedmioty
- osobowość
- głos
- zasady ciągłości

Generator nie powinien wymyślać wyglądu postaci od nowa dla każdego ujęcia.

## Aktualne postacie

- Hanys — zielony, górnik/budowniczy, kilof
- Hopla — różowa, zwiadowczyni, plecak
- Fachura — niebieski, górnik, dwa świecące kilofy
- Podciep — fioletowy, latarnik, lampa

## API bridge — gotowe

`server.py` udostępnia:

- `GET /health` — sprawdza API i dostępność ComfyUI
- `GET /characters` — zwraca kanoniczną bazę Beboków
- `POST /generate` — przyjmuje postać + opis sceny + opcjonalny seed i wysyła workflow do ComfyUI
- `GET /jobs/{prompt_id}` — pobiera status/wynik joba z ComfyUI

Uruchomienie lokalne:

```bash
cd video-engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn server:app --reload --port 8000
```

ComfyUI powinno działać domyślnie na `http://127.0.0.1:8188` albo adres należy ustawić w `COMFYUI_URL`.

## Workflow ComfyUI

`comfyui_workflow.template.json` jest kontraktem, a nie gotowym workflow modelu. Celowo nie wpisujemy na sztywno nazw custom-node'ów, ponieważ Wan/LTX mogą być zainstalowane przez różne rozszerzenia ComfyUI.

W ComfyUI należy:

1. zainstalować wybrany open-source video model i jego custom nodes,
2. zbudować działające image-to-video workflow,
3. wyeksportować je w formacie API,
4. podmienić wartości wejściowe na placeholdery `{{PROMPT}}` i `{{SEED}}`,
5. dla węzła obrazu referencyjnego użyć `{{REFERENCE_IMAGE}}` po dodaniu adaptera uploadu referencji.

To pozwala zmienić Wan/LTX bez przebudowy API Shopify.

## Generowanie odcinka

1. Użytkownik podaje pomysł.
2. Story Engine tworzy sceny i dialogi.
3. Character Registry wybiera kanoniczne postacie.
4. Każda scena dostaje referencje postaci, lokację, kamerę, seed i stan poprzedniej sceny.
5. ComfyUI wykonuje workflow.
6. Wyniki są zapisywane jako osobne ujęcia.
7. Pipeline montuje odcinek.
8. Shopify może wyświetlić gotowy film.

## Następny krok

Podłączamy konkretny workflow Wan/LTX i robimy pierwszy test: **Fachura znajduje magiczną skrzynię pod Spodkiem**. Dopiero po przejściu tego testu podpinamy przycisk generatora do Shopify.

## Ważne

Obecne zdjęcia są referencjami wizualnymi. Nie są jeszcze modelami 3D ani wagami LoRA/Checkpoint. Docelowo możemy dodać LoRA/adaptery dla każdej postaci, jeśli uzyskamy odpowiednie materiały treningowe i zgodę na ich użycie.
