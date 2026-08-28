# BEBOKI — PAMIĘĆ PROJEKTU

> Źródło prawdy dla dalszego rozwoju gry. Aktualizujemy po ważnych decyzjach, researchu, błędach i wdrożeniach.

## 1. CEL GRY
Beboki to mobilna gra przeglądarkowa łącząca **Lemmings + Heroes of Might and Magic + Penguin Club**, osadzona w Katowicach.

Pętla: **osada → mapa Katowic → misja → wybór drużyny → eksploracja → ratowanie psów → nagrody → rozwój osady → kolejne lokacje**.

Nie chcemy generycznego fantasy. Katowice, piwnice, kopalnie, kamienice, Beboki i psy mają być rdzeniem świata.

## 2. POSTACIE
- **Hanys** — kopanie, zawały, budowanie.
- **Hopla** — zwiad, tropienie, ukryte przejścia.
- **Fachura** — mechanizmy, urządzenia, naprawy.
- **Podciep** — światło, sekrety, ochrona.

### Kanon wyglądu
Cztery dostarczone przez użytkownika grafiki są referencją kanoniczną. **Nie generować nowych wariantów wyglądu postaci bez potrzeby.** Docelowo model 3D ma zachować rozpoznawalność twarzy, futra, fryzury, stroju, kolorystyki i charakterystycznych rekwizytów.

## 3. GAMEPLAY — DOCZELOWY MODEL
Gracz nie steruje każdą postacią jak w zwykłym RPG. Wydaje **polecenia jednostkom**.

Przykład:
- kliknij miejsce → Bebok znajduje drogę;
- kliknij zawał → Hanys może kopać;
- kliknij podejrzane miejsce → Hopla może zbadać;
- kliknij mechanizm → Fachura może naprawić;
- kliknij ciemny obszar → Podciep może oświetlić.

Każda akcja ma koszt/czas i zmienia stan świata. Misje mają cele i wymagają kombinowania rolami.

## 4. PIERWSZY VERTICAL SLICE
Jedna grywalna piwnica: tilemap, ściany i kolizje, grid, pathfinding, 4 Beboki jako jednostki, zawał, mechanizm, ciemny obszar, ukryte przejście, 6 kości, pies jako cel, nagroda i powrót do osady.

## 5. KIERUNEK 3D — NOWY TOR R&D
Dodano `world3d.html` jako pierwszy prototyp sceny 3D.

Cel: przejście od płaskich obrazków do **prawdziwej sceny 3D + animowanych avatarów + zachowania AI**.

Stack testowy:
- Three.js 0.180
- WebGL teraz; WebGPU można włączyć później
- OrbitControls
- GLB/GLTF jako docelowy format modeli
- VRM/three-vrm jako kandydat dla avatarów

`world3d.html` jest prototypem technologii, nie finalnym wyglądem Beboków. Tymczasowa geometria proceduralna służy wyłącznie do sprawdzenia sceny, kamery, oświetlenia, interakcji i click-to-move. **Nie traktować jej jako zastępstwa dla kanonicznych modeli.**

Docelowy pipeline avatarów:
**kanoniczny obraz → image-to-3D → czyszczenie modelu → tekstury → rig → animacje → GLB/VRM → gra**.

Docelowy pipeline „żywego organizmu”:
**AI decyzja → system zachowania → nawigacja → animacja → reakcja świata → pamięć stanu**.
AI nie powinno sterować fizyką klatka po klatce.

## 6. ARCHITEKTURA
- Repo: `bajerskim11-eng/beboki-gra`
- Hosting: Vercel
- Obecny silnik 2D: **Phaser 4**.
- Tor eksperymentalny 3D: **Three.js**.
- Mapy 2D: **Tiled** lub Phaser Tilemap Editor.
- Ruch/grid 2D: **Grid Engine**.
- Pathfinding: Grid Engine/A* na małych mapach; navmesh dopiero przy dużych, nieregularnych lokacjach.
- Assety: Shopify CDN lub repo `assets/`, zależnie od licencji i stabilności.
- Stan gry: osobny model danych, niezależny od UI.
- Prototyp: localStorage.
- Produkcja: backend/baza (Supabase jest kandydatem) dla kont, postępu, ekwipunku i świata.

## 7. RESEARCH — NAJWAŻNIEJSZE
### Grid Engine — `Annoraaq/grid-engine`
Kompatybilny z Phaser 4, Apache-2.0. Oferuje grid movement, kolizje, pathfinding, collision groups, multi-tile objects, izometrię i ruch 4/8-kierunkowy.

**Decyzja:** bardzo mocny kandydat do integracji zamiast pisania własnego systemu ruchu.

### Phaser RPG Template — `danielart/phaser-rpg-template`
MIT. Tiled maps, sceny/NPC, drzwi i ukryte drzwi, Grid Engine, interakcje. Bazuje na Phaser 3, więc traktować jako wzorzec, nie kopiować bezpośrednio do Phaser 4.

### Phaser Navmesh — `sporadic-labs/phaser-navmesh`
MIT. Pathfinding przez navmesh. Zostawić jako opcję dla dużych, nieregularnych lokacji.

### Phaser Tiled — `englercj/phaser-tiled`
Legacy/stary projekt. **Nie używać.**

### VRM Game Starter — `norio/vrm-game-starter`
Ciekawy kierunek dla przeglądarkowego świata 3D: Three.js, VRM, animacje, IK, kolizje, kamera i sterowanie dotykowe. Traktować jako źródło architektury/inspiracji; przed użyciem kodu sprawdzić aktualny stan repo i licencje assetów.

### three-vrm — `pixiv/three-vrm`
Biblioteka VRM dla Three.js. Kandydat do docelowych avatarów, jeśli pipeline modeli będzie oparty o VRM.

### three-avatar — `VerseEngine/three-avatar`
Kandydat do analizy pod kątem IK, lip-sync, animacji i sterowania avatarami.

### Helbreath Base Game
Obserwować rozwiązania map, NPC, ekwipunku i multiplayera; nie kopiować architektury przed stabilnym vertical slice.

## 8. LICENCJE
Kod i assety oceniamy osobno. MIT/Apache-2.0 kodu nie oznacza automatycznie takiej samej licencji assetów. Nie kopiować assetów bez sprawdzenia.

## 9. ZASADA DALSZEJ PRACY
1. Najpierw czytaj istniejący kod i pamięć.
2. Szukaj sprawdzonych open-source rozwiązań przed pisaniem własnego systemu.
3. Sprawdzaj aktualność repo i licencję.
4. Integruj małe, niezależne elementy.
5. Po każdej większej zmianie testuj deployment.
6. Nie deklaruj „działa” bez weryfikacji.
7. Nie wkładaj kluczy API do frontendu/GitHuba.
8. Nie twórz kolejnych atrap ekranów, jeśli możemy implementować mechanikę.
9. Kanoniczne grafiki Beboków traktuj jako źródło prawdy dla wyglądu.
10. Prototypy 3D mają udowadniać technologię; nie zastępują finalnego art direction.

## 10. BACKLOG PRIORYTETOWY
1. Stabilna aplikacja Phaser 4.
2. Integracja Grid Engine.
3. Pierwsza tilemap piwnicy.
4. Kolizje + grid + pathfinding.
5. Jednostki Beboków i click-to-move.
6. System umiejętności/interakcji z obiektami.
7. Pies i warunki zwycięstwa.
8. Nagrody + stan misji.
9. **3D tech demo: scena + kamera + 4 tymczasowe rigy + click-to-move.**
10. **Pipeline prawdziwego modelu 3D Hanysa z kanonicznej referencji.**
11. Osada jako prawdziwa scena gry.
12. Mapa Katowic.
13. Backend/Supabase.
14. Social/multiplayer.
15. AR jako późniejsza warstwa świata.
