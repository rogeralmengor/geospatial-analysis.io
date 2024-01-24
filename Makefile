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
test: 
	#test
deploy: 
	#deploy
all: install lint test deploy