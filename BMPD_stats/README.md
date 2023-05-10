# BMPD stats

This folder contains lists of MuseScore files and exported stave ids used in making BMPD dataset. The files have following content:

- all_mscz_files.txt: list of MuseScore files that was processed
- all_parts.txt: list of all polyphonic parts selected from musescore files after part_splitting
- all_staves.txt: stave IDs for separated staves used (not every exported stave is used, BMPD uses mostly just polyphonic staves and high-density staves (40 and more notes per measure)
- trn_staves.txt: stave IDs used for training set
- tst_staves.txt: stave IDs used for validation set
- tst_hard_staves.txt: stave IDs used in BMPD-Hard subset


