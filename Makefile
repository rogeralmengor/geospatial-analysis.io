install: 
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	python -m textblob.download_corpora
format: 
	#format code
	black *.py
	black src/*
lint: 
	pylint --disable=R,C *.py src/*.py
mypy:
	mypy *.py src/*.py
build: 
	# build container
test: 
	python -m pytest -vv --cov=src --cov=main test_*.py
deploy: 
	#deploy
all: install format lint mypy build test deploy