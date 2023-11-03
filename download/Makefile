requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

clean:
	rm -rf backend.zip frontend.zip app.zip

format:
	black .

lint:
	black --check .
	flake8 . --max-line-length=100
	pydocstyle .

install:
	unzip backend.zip -d ../
	unzip frontend.zip -d ../
	unzip app.zip -d ../
