# Pipeline produkcji odcinka

1. Autor opisuje scenę.
2. Ollama tworzy scenariusz + shot list.
3. Wynik zapisuje się do pamięci SQLite.
4. Generator obrazu tworzy keyframe.
5. Autor akceptuje keyframe.
6. Wan2.1/LTX animuje keyframe.
7. FFmpeg składa klipy.
8. Dodajemy narrację, muzykę, efekty i napisy.
9. Finalny MP4 trafia do YouTube.

## Format jednego ujęcia

```json
{
  "episode": 1,
  "shot": 4,
  "duration": 7,
  "location": "Katowice, stara kamienica",
  "characters": ["Hopla", "Podciep", "Hanys", "Fachura", "pies"],
  "image_prompt": "...",
  "video_prompt": "...",
  "dialogue": "...",
  "sfx": ["deszcz", "szczekanie", "kroki"]
}
```

## Strategia jakości

Nie generujemy od razu 10 minut filmu. Najpierw 8–12 ujęć, każdy keyframe zaakceptowany, każdy klip 5–8 sekund, dopiero potem montaż. Dzięki temu możemy pilnować ciągłości Beboków, lokacji i historii.