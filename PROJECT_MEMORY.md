# BEBOKI — PAMIĘĆ PROJEKTU

> Ten plik jest źródłem prawdy dla dalszego rozwoju gry. Aktualizuj go po ważnych decyzjach, zmianach architektury, odkrytych problemach i znalezionych repozytoriach.

## 1. CEL GRY

Beboki to przeglądarkowa gra mobilna inspirowana połączeniem **Lemmings + Heroes of Might and Magic + Penguin Club**.

Główna pętla:
**osada → mapa Katowic → misja → wybór drużyny → eksploracja → ratowanie psów → nagrody → rozwój osady → kolejne lokacje**.

Świat ma zachować charakter Katowic i Beboków, a nie wyglądać jak generyczna gra fantasy.

## 2. POSTACIE

Podstawowa drużyna:
- Hanys — górnik/budowniczy, kopanie i usuwanie zawałów.
- Hopla — zwiadowczyni, szukanie drogi i ukrytych przejść.
- Fachura — wynalazca, mechanizmy i urządzenia.
- Podciep — latarnik/strażnik, światło i odkrywanie sekretów.

Postacie mają zachować wygląd z dostarczonych przez użytkownika grafik: realistyczne, szczegółowe futro, duże oczy, charakterystyczne stroje robocze, lekko filmowy wygląd. Nie robić ich zbyt bajkowymi ani mrocznymi.

## 3. HISTORIA / ŚWIAT

Psy zaczynają wyczuwać coś pod ziemią i chowają się po piwnicach. Beboki wyruszają, żeby je odnaleźć. Tajemnica prowadzi przez piwnice, kopalnie i Katowice.

Docelowo świat może rozszerzyć się o większą mapę Katowic, lokacje AR, NPC, wydarzenia i rozbudowaną historię.

## 4. UX / PLATFORMY

Priorytet: **telefon i przeglądarka**.

Gra ma działać bez instalacji. Desktop może być wspierany, ale projektowanie zaczynamy mobile-first.

## 5. OBECNA ARCHITEKTURA

- Repo: `bajerskim11-eng/beboki-gra`
- Hosting: Vercel
- Frontend/prototyp: HTML/JS + rozpoczęta integracja Phaser
- Grafiki postaci: Shopify CDN
- Lokalny prototyp zapisu: localStorage
- Wcześniejszy kierunek techniczny dla 3D: React/Three.js na Vercel + NVIDIA TRELLIS przez `/api/generate-3d`; klucz NVIDIA wyłącznie po stronie serwera jako `NVIDIA_API_KEY`.

## 6. KIERUNEK TECHNICZNY GRY

Nie budować kolejnych atrap ekranów. Rozwijać w stronę prawdziwej gry:
- Phaser jako kandydat na silnik 2D przeglądarkowy.
- Tilemapy / grid dla plansz misji.
- Sceny: Osada, Mapa, Misja, Budynek, Nagroda.
- Stan gracza oddzielony od UI.
- Docelowo backend/baza danych dla kont, postępu, ekwipunku i świata.

## 7. REPOZYTORIA / INSPIRACJE

### Pogicity Demo
`twofactor/pogicity-demo`

Warto wykorzystać jako inspirację/źródło architektury dla izometrycznej osady, budynków, gridu i city-buildera. Kod repo jest MIT, ale nie zakładać, że wszystkie assety graficzne mają tę samą licencję.

### Phaser RPG Template
`remarkablegames/phaser-rpg`

Warto wykorzystać jako inspirację dla map, NPC, scen, interakcji i struktury RPG. Licencję sprawdzać przed kopiowaniem kodu/assetów.

### Phaser
`phaserjs/phaser`

Główny kandydat na silnik gry 2D w przeglądarce.

## 8. ZASADA DALSZEJ PRACY

Przed implementacją większej funkcji:
1. Sprawdź istniejący kod/repo.
2. Sprawdź, czy istnieje gotowe open-source repo lub biblioteka, którą można legalnie wykorzystać.
3. Sprawdź licencję kodu i assetów osobno.
4. Nie twórz ponownie rzeczy, które można stabilnie wykorzystać.
5. Po każdej większej zmianie zapisz decyzję tutaj.
6. Po wdrożeniu sprawdź deployment i działanie strony — nie deklaruj „działa”, jeśli nie zostało zweryfikowane.

## 9. BACKLOG — NAJBLIŻSZE

1. Stabilny ekran startowy i logowanie.
2. Osada z prawdziwą grafiką/sceną.
3. Klikalne budynki.
4. Mapa Katowic.
5. Pierwsza prawdziwa plansza tilemap.
6. Ruch Beboków po planszy.
7. Umiejętności postaci wpływające na środowisko.
8. Pies jako aktywny cel misji.
9. System nagród i ekwipunku.
10. Rozwój osady.
11. Konto + backend.
12. Multiplayer/social features w późniejszym etapie.

## 10. CZEGO UNIKAĆ

- Generycznego fantasy zamiast Katowic.
- Nadmiernie bajkowego stylu.
- Nadmiernie mrocznej grafiki.
- Samych ekranów demonstracyjnych bez mechaniki.
- Wrzucania przypadkowych assetów bez sprawdzenia licencji.
- Umieszczania kluczy API w frontendzie/GitHubie.
- Twierdzenia, że wdrożenie działa bez faktycznej weryfikacji.
