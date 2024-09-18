# Musescore pipeline #100

<aside>
💡 Vychází z pipeline #45, #47, #48, viz [MuseScore dataset pipelines](https://www.notion.so/MuseScore-dataset-f141d78cfe0a447bbb599d52a322eab0?pvs=21)
se zásadní změnou: jedou na LINUX UBUNTU 🐧
</aside>

<aside>
💡 DŮLEŽITÝ NASTAVENÍ Musescore → Edit → Preferences → Import → Import layout + page breaks
</aside>

- **0_orig_mscz**: original musescore soubory
- **1_musicxml_by_M3_CLI**: Mscz → musicxml  MmuseScore 3 native CLI
    - 2. možnost je **M4_CLI**, ale pak to může být nekonzistentní, protože export XML do png potřebuju zase M3
- **2_musicxml_parts**: Separate to parts with `part_splitter.py`
    - Zmenšení stránek pomocí `<page-layout><page-height>400>>`
    - Nastavení odsazení prvního řádku stránky pomocí `<top-system-distance>`  (v print new-page)
- **3_img_pages**: Musicxml → images using Musescore4 CLI
- **4_img_staves:** Rename already separated staves with  `img_to_staves.py`  (and setting to just rename it, with negative `--staff_count`)
- **5_labels_semantic**: **2_musicxml_parts** → labels using `polyphonic-omr/label_gen/genlabels.py`
- **6_copied_pairs**: copied corresponding pairs of **5_labels_semantic + 4_img_staves** using `matchmaker.py`  + `check_staff_lines.py`  + `symbol_converter.py`
    - symbol_converter.py - shorten semantic to r”s+emantic”
- **7_lmdb_db: 6_copied_pairs →** lmdb image database + shortened and split labels
    - lmdb_generator.py - images to lmdb with given keys
    - label_set_splitter.py - split whole label file to two randomized sets of labels for validation set and training set
