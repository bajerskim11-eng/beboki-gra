# ComfyUI workflows

Tutaj wkładamy **API format** workflowów eksportowanych z ComfyUI.

## image_api.json

Workflow powinien generować pojedynczy obraz. Ustaw w `.env` identyfikator noda z promptem: `COMFY_POSITIVE_NODE=...`

Opcjonalnie: `COMFY_NEGATIVE_NODE`, `COMFY_SEED_NODE`.

## video_api.json

Workflow powinien przyjmować prompt i generować krótki klip image-to-video albo text-to-video.

Najlepszy kierunek dla tej bajki: **Wan2.1** dla prostego I2V/T2V, **LTX-2** gdy chcemy później łączyć audio + video.

Studio celowo nie hard-code'uje numerów nodów, bo użytkownik może zmienić workflow.

## Ważne

Eksportuj przez **Save (API Format)** w ComfyUI, nie zwykły workflow UI JSON.