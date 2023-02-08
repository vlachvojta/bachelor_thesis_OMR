# Nastrel prezentace semestralniho projektu
## Pokyny
- 4 minuty prezentace + 4 minuty diskuze

Slajdy
- 4-7 slajdů ve formátu PPTX/PDF.

Co ano
- Mluvit o SVÉ práci, lidem, kteří jsou odborně celkem zdatní.

Co ne
- Obecné úvody, přednášky o technologiích, vysvětlování něčeho, co není Vaše.

## Obsah prezentace + stručný popis
- Motivace
  - Hudebníci
- Cíl práce
  - OMR = optical music recognition
  - Simple znázorňující grafika - monofonní + polyfonní example???
  - Zmínit End to End ? (Ne pipeline)
- Návrh řešení
  - VGG/CNN
  - Transformery dekodér + enkodér   - TODO jak to znázornit?
  - Trénování
- Informace o stavu řešení
  - Dataset monofonní OK + velikost datasetu
  - Experimenty monofonní OK, představit experimenty pomocí nějaký hezký grafiky (cer + wer)
- Plán další práce
  - Dodělání polyphonic datasetu
  - Nový zápis + Experimenty s různými ostatními
  - Vytvoření transformeru + trénování

## TODOS
- wers for checkpoints
- ?wtf VGG/CNN?
- sone charts and stuf...
- grafika na END-TO-END vs pipeline


https://link.springer.com/article/10.1007/s13735-012-0004-6
https://link.springer.com/content/pdf/10.1007/s13735-012-0004-6.pdf?pdf=button%20sticky

...
<Note>
    <durationType>quarter</durationType>
    <pitch>60</pitch>
</Note>
<Note>
    <durationType>quarter</durationType>
    <pitch>64</pitch>
</Note>
<Note>
    <durationType>quarter</durationType>
    <pitch>67</pitch>
</Note>
<Rest>
    <durationType>quarter</durationType>
</Rest>
...


</Measure>
<Measure number="2">
    <Chord>
        <durationType>quarter</durationType>
        <Note>
            <pitch>60</pitch>
            <tpc>14</tpc>
        </Note>
    </Chord>
    <Chord>
          <durationType>quarter</durationType>
          <Note>
            <pitch>64</pitch>
            <tpc>18</tpc>
            </Note>
          </Chord>
        <Chord>
          <durationType>quarter</durationType>
          <Note>
            <pitch>67</pitch>
            <tpc>15</tpc>
            </Note>
          </Chord>
