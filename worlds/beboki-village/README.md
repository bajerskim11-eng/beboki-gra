# Beboki Village — Image2World pipeline

## Cel

`village.jpg` jest kanoniczną referencją środowiska. Nie generujemy kolejnego obrazka zamiast świata. Chcemy uzyskać prawdziwy, nawigowalny świat 3D:

`image -> Image2World -> SPZ/PLY + collision GLB -> Spark/Three.js -> gra`

## Wybrane repo

**Image2World**: https://github.com/TingdeLiu/Image2world

Repo jest MIT i potrafi z pojedynczego zdjęcia przygotować Gaussian Splat + siatkę kolizji + `scene.json`. Lokalny pipeline używa GPU NVIDIA; alternatywnie może użyć World Labs Marble.

**Spark 2.1**: https://github.com/sparkjsdev/spark

Spark jest MIT i jest rendererem 3D Gaussian Splatting dla Three.js/WebGL2. Obsługuje SPZ/PLY i LoD oraz łączenie splatów z normalnymi obiektami 3D.

## Źródło

Shopify CDN: https://cdn.shopify.com/s/files/1/1019/1903/1622/files/beboki-village-source.jpg?v=1787899947

## Docelowa struktura wygenerowanego świata

```text
worlds/beboki-village/
  project.json
  scene.json
  output/
    world/
      0-world-500k.spz
      0-world-150k.spz
      0-world-100k.spz
      0-world.glb
      0-world.json
```

`world3d-v4.html` automatycznie próbuje załadować `/worlds/beboki-village/0-world-500k.spz` przez Spark. Jeśli pliku jeszcze nie ma, pokazuje kanoniczne zdjęcie referencyjne zamiast udawać, że scena 3D została wygenerowana.

## Generacja na NVIDIA

1. Sklonuj Image2World.
2. Uruchom backend zgodnie z jego `backend/README.md`.
3. Otwórz frontend Image2World.
4. Utwórz nowy świat z powyższego zdjęcia.
5. Wybierz lokalny backend SHARP, jeśli chcemy bezpłatnie użyć własnego GPU.
6. Po wygenerowaniu skopiuj wygenerowane SPZ/GLB/scene.json do tego katalogu.
7. Otwórz `world3d-v4.html`.

## Ważne

Single-view reconstruction nie odtwarza niewidocznej strony świata. Dlatego docelowo chcemy wygenerować kilka ujęć tej samej osady albo użyć modelu generującego zamknięty świat. Image2World dokumentuje tę różnicę między lokalną rekonstrukcją SHARP a generatywnym Marble.

## Kanon Beboków

Hanys, Hopla, Fachura i Podciep muszą zachować wygląd z dostarczonych przez właściciela projektu referencji. Środowisko może być generowane, ale wygląd postaci nie może być reinterpretowany.
