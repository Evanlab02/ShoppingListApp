.PHONY: install

.venv:
	uv venv

requirements.txt: .venv
	uv pip compile --no-annotate requirements.in -o requirements.txt

install: .venv requirements.txt
	uv pip install -r requirements.txt
