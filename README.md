# Neural networks for optical music recognition
My bachelor thesis on FIT (V|B)ut Brno, assembled in 2022/2023

Final thesis in CZ: [Automaticke_rozpoznani_hudebnich_zapisu_pomoci_neuronovych_siti.pdf](Automaticke_rozpoznani_hudebnich_zapisu_pomoci_neuronovych_siti.pdf)

## Abstract
This thesis consideres the problem of optical music recognition from images to text using Artificial inteligence and neural networks. I have choosed particularly the field of printed polyphonic music (more notes and voices at the same time). The goal of this thesis is to create a model capable of recognising complex notations and its accuracy compare with previous literature and other known models. I solved the chosen problem by utilizing the Vision Transformer architecture, where I tested several network variants to find the most powerful one. And by creating a new dataset with polyphonic music. The work presents the process of creating the dataset by synthesizing images from MusicXML format using the MuseScore program. The most successful variant of the Vision Transformer architecture achieves an error rate of only 7.86%, which is very promising for further development and utilization. The main finding is that the architecture has the potential to dominate in this field, just as it does in other areas of research, and there is a functional solution for the specific task of polyphonic music notation recognition, which has been only up for a debate until now. 

## Keywords
Computer vision, neural networks, transformer, optical music recognition, OMR, polyphonic music, preparation of training data

## Reference
VLACH, Vojtěch. NEURAL NETWORKS FOR OPTICAL MUSIC RECOGNITION. Brno, 2023. Bachelor’s thesis. Brno University of Technology, Faculty of Information Technology. Supervisor Ing. Michal Hradiš, Ph.D.

## Codebase
Codebase consists of individual scripts where each one has its own purpose and documentation at the top.

There are following folders in this repository
* BMPD_stats - containing statistics about the new BMPD dataset
* dataset-utilities - python scripts for working with both PrIMuS and BMPD datasets
* experiments - python scripts for experiments with CRNN and Transformer models.
* layout_detection - python scripts for training and detecting layout detection of staves on pages using ultralytics YOLOv8 models (added AFTER submission of thesis)
* musescore-dataset-utilities - python scripts used for creating the BMPD dataset itself.
* primus_stats - statistics about PrIMuS dataset

## Zadání práce (Assignement in CZ)
1. Prostudujte základy konvolučních neuronových sítí, sítí založených na attention a autoregresivních modelů.
2. Vytvořte si přehled o současných metodách automatického rozpoznání hudebního zápisu z obrazu.
3. Navrhněte metodu schopnou automaticky rozpoznávat hudební zápis z obrazu nebo upravte vhodnou existující metodu.
4. Obstarejte si databázi vhodnou pro experimenty. Můžete rozšířit existující databázi.
5. Implementujte navrženou metodu a proveďte experimenty nad datovou sadou.
6. Porovnejte dosažené výsledky a diskutujte možnosti budoucího vývoje.
7. Vytvořte jednoduchou demonstrační aplikaci, která bude využívat implementovaný systém.
8. Vytvořte stručné video prezentující vaši práci, její cíle a výsledky.
* streamlit_helpers - one script used to show dataframe in a web browser using streamlit server
* translators - dictionaries used in shortening ground-truths of both PrIMuS and BMPD datasets.

## Primus dataset links
* dataset downloaded from: https://grfia.dlsi.ua.es/primus/packages/primusCalvoRizoAppliedSciences2018.tgz
* Info and other links: https://grfia.dlsi.ua.es/primus/
* Code for experiments: https://github.com/OMR-Research/tf-end-to-end
