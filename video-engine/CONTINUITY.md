# Ciągłość postaci

Nie próbujemy zachować tożsamości Beboka samym promptem. Każda postać ma własny zestaw referencji i identyfikator.

## Warstwy ciągłości

1. **Reference pack** – zatwierdzone obrazy postaci z wielu kątów.
2. **Character metadata** – wygląd, ubranie, kolory, akcesoria, osobowość.
3. **Seed / shot metadata** – zapis parametrów każdego ujęcia.
4. **Keyframes** – pierwsza/ostatnia klatka poprzedniego ujęcia mogą zasilać następne.
5. **LoRA / adapter** – jeśli referencje nie wystarczą, trening konkretnego Beboka.
6. **Human approval** – ujęcie trafia do biblioteki dopiero po zatwierdzeniu.

## Biblioteka historii

Każdy odcinek powinien zapisywać:

- episodeId
- sceneId
- characterIds
- locationId
- prompt
- negativePrompt
- seed
- model
- workflowVersion
- inputReferences
- outputVideo

Dzięki temu możemy później odtworzyć lub poprawić dowolne ujęcie bez utraty kanonu.
