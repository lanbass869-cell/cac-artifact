.PHONY: all scan classify downstream clean

all: scan classify

scan:
	MEM_DB=./synthetic_memory.db python scan_contradictions.py

classify:
	python classify_contradictions.py

downstream:
	python downstream_contradiction_test.py

generate:
	python generate_synthetic_db.py

clean:
	rm -f _scan_contradictions_results.json _contradiction_classification.json
