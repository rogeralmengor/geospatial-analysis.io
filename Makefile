install: 
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	python -m textblob.download_corpora
format: 
	#format code
	black 
	black src/*.py
lint: 
	pylint --disable=R,C src/*.py
mypy:
	mypy src/*.py
build: 
	docker build -t deploy-fastapi .
test: 
	python -m pytest -vv --cov=src --cov=main test_*.py
run: 
	docker run -p 127.0.0.1:8080:8080 fa1cf0977a0f
deploy: 
	#docker build -t deploy-fastapi
all: install format lint mypy build test deploy