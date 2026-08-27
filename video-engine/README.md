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

## Generowanie odcinka

1. Użytkownik podaje pomysł.
2. Story Engine tworzy sceny i dialogi.
3. Character Registry wybiera kanoniczne postacie.
4. Każda scena dostaje referencje postaci, lokację, kamerę, seed i stan poprzedniej sceny.
5. ComfyUI wykonuje workflow.
6. Wyniki są zapisywane jako osobne ujęcia.
7. Pipeline montuje odcinek.
8. Shopify może wyświetlić gotowy film.

## Ważne

Obecne zdjęcia są referencjami wizualnymi. Nie są jeszcze modelami 3D ani wagami LoRA/Checkpoint. W następnym kroku można dodać LoRA/adaptery dla każdej postaci, jeśli uzyskamy odpowiednie materiały treningowe i zgodę na ich użycie.
