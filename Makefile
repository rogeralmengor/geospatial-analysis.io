install: 
	# install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format: 
	#format code
	black *.py
	black src/*
lint: 
	pylint --disable=R,C *.py src/*.py
mypy:
	mypy --install-types
	mypy *.py src/*.py
build: 
	# build container
test: 
	python -m pytest -vv *.py --cov=src test_logic.py
deploy: 
	#deploy
all: install format lint mypy build test deploy