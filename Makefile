# Makefile para projeto de Ciência de Dados

.PHONY: help install run clean test format lint

help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instala dependências"
	@echo "  make run        - Executa o dashboard Streamlit"
	@echo "  make clean      - Remove arquivos temporários"
	@echo "  make test       - Executa testes"
	@echo "  make format     - Formata código com black"
	@echo "  make lint       - Verifica código com ruff"

install:
	pip install -r requirements.txt

run:
	streamlit run app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage

test:
	pytest tests/ -v --cov=src --cov-report=html

format:
	black src/ app.py

lint:
	ruff check src/ app.py

setup-dirs:
	mkdir -p data/external
	mkdir -p data/processed
	mkdir -p reports/figs_interactive
	mkdir -p reports/figs_static
	mkdir -p models
