# BEBOKI — RESEARCH / REPO RADAR

## 2026-08-28

### Phaser
Repo: https://github.com/phaserjs/phaser
Licencja: MIT.
Status: **GŁÓWNY KANDYDAT NA SILNIK 2D**.
Dlaczego: web/mobile, WebGL/Canvas, sceny, fizyka, input, kamery, tilemapy, animacje. Aktualne repo opisuje Phaser 4.2.1 i oficjalny generator projektów. 
Źródło: https://github.com/phaserjs/phaser

### Phaser Tiled
Repo: https://github.com/englercj/phaser-tiled
Licencja: MIT.
Status: **TYLKO REFERENCJA / NIE INTEGROWAĆ TERAZ**.
Opis: optymalizacja tilemap dla dużych map Tiled. Projekt jest starszy i dokumentacja wskazuje konkretne starsze wersje Tiled/Phaser, więc nie chcemy go wciągać do nowej architektury bez potrzeby.
Źródło: https://github.com/englercj/phaser-tiled

### melonJS
Repo: https://github.com/melonjs/melonJS
Licencja: MIT.
Status: **ALTERNATYWA, NIE ZMIENIAMY SILNIKA**.
Opis: nowoczesny silnik 2D/2.5D, tilemapy, Tiled, WebGPU/WebGL/Canvas, fizyka i sceny. Ciekawy do researchu, ale równoległe używanie z Phaserem zwiększyłoby złożoność.
Źródło: https://github.com/melonjs/melonJS

## Decyzja
Na obecnym etapie nie dokładamy drugiego silnika. Budujemy jedną spójną grę na Phaserze i wykorzystujemy Tiled do projektowania plansz.

## Następny research
- gotowe tilemapy / edytory poziomów kompatybilne z Phaser 4
- system pathfindingu A* do poruszania Beboków
- sprite sheets / atlas dla animacji postaci
- system dialogów i questów
- zapis stanu gry
- Supabase auth + database, kiedy gameplay będzie stabilny
- assety CC0/MIT/CC-BY z wyraźną możliwością użycia komercyjnego

## Zasada licencyjna
Kod i assety oceniamy osobno. Nie kopiujemy assetów z repo tylko dlatego, że samo repo ma MIT. Każdy zewnętrzny asset musi mieć sprawdzoną licencję i zapis w tym pliku.
