# Bachelor thesis OMR
My bachelor thesis on FIT (V|B)ut Brno, assembled in 2022/2023

Final thesis in CZ is available in: [Automaticke_rozpoznani_hudebnich_zapisu_pomoci_neuronovych_siti.pdf](Automaticke_rozpoznani_hudebnich_zapisu_pomoci_neuronovych_siti.pdf)

## Primus links
* dataset downloaded from: https://grfia.dlsi.ua.es/primus/packages/primusCalvoRizoAppliedSciences2018.tgz
* Info and other links: https://grfia.dlsi.ua.es/primus/
* Code for experiments: https://github.com/OMR-Research/tf-end-to-end

## Zadání práce
1. Prostudujte základy konvolučních neuronových sítí, sítí založených na attention a autoregresivních modelů.
2. Vytvořte si přehled o současných metodách automatického rozpoznání hudebního zápisu z obrazu.
3. Navrhněte metodu schopnou automaticky rozpoznávat hudební zápis z obrazu nebo upravte vhodnou existující metodu.
4. Obstarejte si databázi vhodnou pro experimenty. Můžete rozšířit existující databázi.
5. Implementujte navrženou metodu a proveďte experimenty nad datovou sadou.
6. Porovnejte dosažené výsledky a diskutujte možnosti budoucího vývoje.
7. Vytvořte jednoduchou demonstrační aplikaci, která bude využívat implementovaný systém.
8. Vytvořte stručné video prezentující vaši práci, její cíle a výsledky.

## Codebase

Codebase consists of individual scripts where each one has its own purpose and documentation at the top.

There following folders in this repository:
* BMPD_stats - containing statistics about the new BMPD dataset
* dataset-utilities - python scripts for working with both PrIMuS and BMPD datasets
* experiments - python scripts for experiments with CRNN and Transformer models.
* musescore-dataset-utilities - python scripts used for creating the BMPD dataset itself.
* primus_stats - statistics about PrIMuS dataset
* streamlit_helpers - one script used to show dataframe in a web browser using streamlit server
* translators - dictionaries used in shortening ground-truths of both PrIMuS and BMPD datasets.
