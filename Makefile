# Configurações de Caminhos
PYTHON = python3
REGEX_FILE = examples/scanner/regex.txt
TEST_DIR = examples/parser

# Pega todos os arquivos .rkt dentro da pasta de testes
TEST_FILES = $(wildcard $(TEST_DIR)/*.rkt)

# Alvo padrão
all: run

# Gera o scanner (essencial para qualquer teste)
scanner:
	@echo "Gerando scanner..."
	$(PYTHON) gerar_scanner.py $(REGEX_FILE)

# Bateria de testes
test: scanner
	@echo "Iniciando testes em $(TEST_DIR)..."
	@for file in $(TEST_FILES); do \
		echo "\n--------------------------------------------------"; \
		echo "Testando: $$file"; \
		$(PYTHON) analisar_sintaxe.py $$file; \
		echo "--------------------------------------------------"; \
		echo "Pressione ENTER para o proximo teste..."; \
		read _ ; \
	done
	@echo "\nBateria de testes concluida!"

# Limpeza
clean:
	@echo "Limpando ambiente..."
	rm -rf __pycache__ scanner_gen/__pycache__ parser/__pycache__
	rm -f tabela_afd.json

.PHONY: all scanner run test clean