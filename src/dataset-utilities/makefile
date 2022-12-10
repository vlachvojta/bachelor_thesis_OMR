PY=python3.8
GUS=get_unique_symbols.py
GUS_ALL=../../../datasets/primus_stats/all_unique_symbols.json

all: unique_symbols_test

get_all_unique_symbols:
	$(PY) $(GUS) -F ../../../datasets/primus_untouched/package_a*/ -o $(GUS_ALL) -d $(GUS_ALL)

convert_symbols:
	./symbol_converter.py -i ../../primus_stats/test_data/000051650-1_1_1.agnostic -o symbols_converted.agnostic

unique_symbols_test:
	$(PY) $(GUS) -f test_data/000051650-1_1_1*

clean:
	rm -rf __pycache__
