.PHONY: help install deps seed run test docs clean build full-refresh snapshot

help:
	@echo "Available commands:"
	@echo "  make install       - Install Python dependencies"
	@echo "  make deps          - Install dbt packages"
	@echo "  make seed          - Load seed data"
	@echo "  make run           - Run all models"
	@echo "  make test          - Run all tests"
	@echo "  make docs          - Generate and serve documentation"
	@echo "  make clean         - Clean target and dbt_packages directories"
	@echo "  make build         - Full build (deps, seed, run, test)"
	@echo "  make full-refresh  - Run models with full refresh"
	@echo "  make snapshot      - Run snapshots"

install:
	pip install -r requirements.txt

deps:
	dbt deps

seed:
	dbt seed

run:
	dbt run

test:
	dbt test

docs:
	dbt docs generate
	dbt docs serve

clean:
	rm -rf target/
	rm -rf dbt_packages/
	rm -f *.duckdb
	rm -f *.duckdb.wal

build: deps seed run test
	@echo "Build complete!"

full-refresh:
	dbt run --full-refresh

snapshot:
	dbt snapshot
