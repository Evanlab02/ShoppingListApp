.PHONY: requirements serve build

clean:
	rm -rf site

requirements:
	uv pip compile requirements.in -o requirements.txt

serve:
	uv run mkdocs serve

build:
	uv run mkdocs build
