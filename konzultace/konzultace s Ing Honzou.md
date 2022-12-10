# "konzultace" s Ing. Honzou

Počet iterací > 5000

## Na githubu
pytorch_ctc + datasets, ostatní ignoruju...

### pytorch_ctc
- net_definitions.py - dict se sítema a co dělaj...
#### nets - rozdelení stagí, backbones=(CNN, pool)...
1. net_michal - VGG
2. net_recurenct - od Honzy...
   - taky ezy CNN podle Honzový diplomky
3. moje net_něco
   - proste moje sit ezy pezy...


**Radši jet master hehee...**


##### pytorch_ocr/train_pytorch_ocr.py nebo tak něco
 - to je ten hlavní vstupní skript (hned pod train.sh jakoby...)
 - Char_set = all by default **ALE musím si udělat svůůjj uuuaaaa**
 - sample-similar-length - BACHA, pokud mám málo dat, může zanášet BIAS, idk...
 - loading_proccesses - pocet jader, který chci (na metacentru musí být +1, ještě ten trénovací jkb...)

 - net - jaky model chci

 - Adam by default
 - learning_rate + bath_size

 - save_step - savuje snapshot
 - show_trans + --show_dir   (dělá snapshoty v každým test_step)

 - warm_up (learning_rate dává postupně jakoby polynom křivku, aby to hnedka nevybouchlo)

**train_step(batch)** - to je ten actual step

##### pytorch_ocr/training_ctc.py

- forward, backward, loss...

##### pytorch_ocr/transformer.py



### datasets
- něco s tím LBDM a tak...
- inicializace, batceh, mappers...

- To hlavní je:
	- data_sampler.py
	- data_buffer.py
	- dataset.py
- Další věci


## Dotazy:
větev - master

přiklad toho LBDM - online

