install: 
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	python -m textblob.download_corpora
format: 
	#format code
	black src/*.py
lint: 
	pylint --disable=R,C src/*.py
mypy:
	mypy src/*.py
test: 
	python -m pytest -vv --cov=src --cov=main src/test_*.py
all: install format lint mypy test