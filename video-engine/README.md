# Beboki Video Engine

Architektura generatora historii Beboków.

## Cel

- stała biblioteka postaci Beboków
- generowanie scen z wybranym Bebokiem
- image-to-video / keyframe workflow
- późniejsze podpięcie ComfyUI API
- publikacja gotowych filmów do Shopify

## Planowany pipeline

`Shopify / Studio -> Story Planner -> Character Registry -> ComfyUI -> LTX/Wan -> Storage -> Shopify`

## Model

Na start używamy warstwy adaptera, żeby można było przełączać modele bez przebudowy aplikacji. Preferowany pierwszy eksperyment: LTX-2.x przez ComfyUI; Wan pozostaje alternatywą dla image-to-video.

## Ważne

Modele i wagi nie są przechowywane w repozytorium Git. Repo zawiera konfigurację, prompty, metadane postaci i workflow. Wagi powinny być pobierane na serwerze GPU.

## Następny krok

Uruchomić ComfyUI na maszynie GPU i wystawić prywatny endpoint. Frontend będzie wysyłał tylko job: postać, scena, styl, długość i seed.
