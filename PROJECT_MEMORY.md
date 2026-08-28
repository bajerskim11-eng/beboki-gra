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

Styl: zgodny z dostarczonymi grafikami; realistyczny/filmowy, sympatyczny, szczegółowy, bez przesadnej bajkowości i bez horroru.

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

## 5. ARCHITEKTURA
- Repo: `bajerskim11-eng/beboki-gra`
- Hosting: Vercel
- Silnik: **Phaser 4**.
- Mapy: **Tiled** lub Phaser Tilemap Editor.
- Ruch/grid: **Grid Engine**.
- Pathfinding: Grid Engine/A* na małych mapach; navmesh dopiero przy dużych, nieregularnych lokacjach.
- Assety: Shopify CDN lub repo `assets/`, zależnie od licencji i stabilności.
- Stan gry: osobny model danych, niezależny od UI.
- Prototyp: localStorage.
- Produkcja: backend/baza (Supabase jest kandydatem) dla kont, postępu, ekwipunku i świata.

## 6. RESEARCH — NAJWAŻNIEJSZE
### Grid Engine — `Annoraaq/grid-engine`
Kompatybilny z Phaser 4, Apache-2.0. Oferuje grid movement, kolizje, pathfinding, collision groups, multi-tile objects, izometrię i ruch 4/8-kierunkowy. Znaleziona wersja: 2.52.1 (maj 2026).

**Decyzja:** bardzo mocny kandydat do integracji zamiast pisania własnego systemu ruchu.

### Phaser RPG Template — `danielart/phaser-rpg-template`
MIT. Tiled maps, sceny/NPC, drzwi i ukryte drzwi, Grid Engine, interakcje. Bazuje na Phaser 3, więc traktować jako wzorzec, nie kopiować bezpośrednio do Phaser 4.

### Phaser Navmesh — `sporadic-labs/phaser-navmesh`
MIT. Pathfinding przez navmesh. Zostawić jako opcję dla dużych, nieregularnych lokacji; niepotrzebny w pierwszej piwnicy.

### Phaser Tiled — `englercj/phaser-tiled`
MIT, ale legacy/stary projekt. **Nie używać.**

### Phaser Grid Movement — `Annoraaq/grid-movement`
Tutorial/demo ruchu gridowego. Do nauki/debugowania; preferować Grid Engine jako bibliotekę.

### Helbreath Base Game
Open-source baza 2D RPG/MMORPG z Phaserem, Reactem i serwerem. Obserwować rozwiązania map, NPC, ekwipunku i multiplayera; nie kopiować architektury przed stabilnym vertical slice.

## 7. LICENCJE
Kod i assety oceniamy osobno. MIT/Apache-2.0 kodu nie oznacza automatycznie takiej samej licencji assetów. Nie kopiować assetów bez sprawdzenia.

## 8. ZASADA DALSZEJ PRACY
1. Najpierw czytaj istniejący kod i pamięć.
2. Szukaj sprawdzonych open-source rozwiązań przed pisaniem własnego systemu.
3. Sprawdzaj aktualność repo i licencję.
4. Integruj małe, niezależne elementy.
5. Po każdej większej zmianie testuj deployment.
6. Nie deklaruj „działa” bez weryfikacji.
7. Nie wkładaj kluczy API do frontendu/GitHuba.
8. Nie twórz kolejnych atrap ekranów, jeśli możemy implementować mechanikę.

## 9. BACKLOG PRIORYTETOWY
1. Stabilna aplikacja Phaser 4.
2. Integracja Grid Engine.
3. Pierwsza tilemap piwnicy.
4. Kolizje + grid + pathfinding.
5. Jednostki Beboków i click-to-move.
6. System umiejętności/interakcji z obiektami.
7. Pies i warunki zwycięstwa.
8. Nagrody + stan misji.
9. Osada jako prawdziwa scena gry.
10. Mapa Katowic.
11. Backend/Supabase.
12. Social/multiplayer.
13. AR jako późniejsza warstwa świata.
