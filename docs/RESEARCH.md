# BEBOKI — RESEARCH / REPO RADAR

## 2026-08-28

### Phaser
Repo: https://github.com/phaserjs/phaser
Licencja: MIT.
Status: **GŁÓWNY SILNIK 2D**.
Dlaczego: web/mobile, WebGL/Canvas, sceny, fizyka, input, kamery, tilemapy, animacje. Phaser 4 ma także GPU tilemap layer dla dużych ortograficznych map.
Źródło: https://github.com/phaserjs/phaser

### Phaser Examples
Repo: https://github.com/phaserjs/examples
Licencja kodu: MIT; assety trzeba oceniać osobno.
Status: **BIBLIOTEKA REFERENCYJNA**.
Opis: setki małych przykładów Phaser, bardzo przydatnych do implementacji konkretnych mechanik zamiast wymyślania ich od zera.
Źródło: https://github.com/pnstickne/phaser-examples

### Phaser By Example
Repo: https://github.com/phaserjs/phaser-by-example
Licencja / assety: sprawdzać osobno przed użyciem komercyjnym.
Status: **REFERENCJA DO GOTOWYCH SCEN I STRUKTURY**.
Opis: 9 pełnych małych gier, część przykładów została przeniesiona do Phaser 4 + TypeScript. Dobre źródło wzorców dla scen, Vite i gameplay loop.
Źródło: https://github.com/phaserjs/phaser-by-example

### Phaser Tiled
Repo: https://github.com/englercj/phaser-tiled
Licencja: MIT.
Status: **TYLKO REFERENCJA / NIE INTEGROWAĆ TERAZ**.
Opis: optymalizacja tilemap dla dużych map Tiled. Projekt jest starszy i dokumentacja wskazuje konkretne starsze wersje Tiled/Phaser, więc nie chcemy go wciągać do nowej architektury bez potrzeby.
Źródło: https://github.com/englercj/phaser-tiled

### BrowserQuest / PhaserQuest
Repo: https://github.com/Jerenaux/phaserquest
Licencja: MIT.
Status: **REFERENCJA DO PÓŹNIEJSZEGO SYSTEMU ŚWIATA**.
Opis: browserowa gra RPG z Phaser, Node.js i socket.io; zawiera mapę Tiled, synchronizację klientów i rozwiązania przydatne przy późniejszym multiplayerze. Nie kopiować starej architektury 1:1.
Źródło: https://github.com/Jerenaux/phaserquest

### melonJS
Repo: https://github.com/melonjs/melonJS
Licencja: MIT.
Status: **ALTERNATYWA, NIE ZMIENIAMY SILNIKA**.
Opis: nowoczesny silnik 2D/2.5D, tilemapy, Tiled, WebGPU/WebGL/Canvas, fizyka i sceny. Ciekawy do researchu, ale równoległe używanie z Phaserem zwiększyłoby złożoność.
Źródło: https://github.com/melonjs/melonJS

### Pogicity Demo
Repo: https://github.com/twofactor/pogicity-demo
Status: **REFERENCJA DLA OSADY / CITY-BUILDERA**.
Opis: izometryczna osada, budynki, grid i logika city-buildera są bliskie temu, jak chcemy rozwijać bazę Beboków. Kod i assety trzeba oceniać osobno.

## Decyzja
Na obecnym etapie nie dokładamy drugiego silnika. Budujemy jedną spójną grę na Phaserze i wykorzystujemy Tiled do projektowania plansz.

## Najbliższy research
1. Tiled + Phaser 4: przygotować pierwszą ortograficzną mapę piwnicy.
2. A* / grid pathfinding dla Beboków.
3. Sprite sheets / atlas i animacje ruchu.
4. System dialogów i questów.
5. Save-state poza localStorage.
6. Supabase Auth + Database dopiero po ustabilizowaniu gameplayu.
7. Assety CC0/MIT/CC-BY z możliwością użycia komercyjnego.

## Zasada licencyjna
Kod i assety oceniamy osobno. Nie kopiujemy assetów z repo tylko dlatego, że samo repo ma MIT. Każdy zewnętrzny asset musi mieć sprawdzoną licencję i zapis w tym pliku.
