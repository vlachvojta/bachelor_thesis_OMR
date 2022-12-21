#!/bin/bash

echo "helo"
echo "==============================="
echo "======= Run files copier ======"
echo "==============================="

./files_copier.py -F ../../../datasets/primus_full_untouched/* -o ../../../datasets/primus_full_converted/ -H 100 -u

echo "==============================="
echo "===== Run lmdb generator ======"
echo "==============================="

./lmdb_generator.py -F ../../../datasets/primus_full_converted -o ../../../datasets/primus_full_converted_lmdb

echo "DONE, fuuuff..."
