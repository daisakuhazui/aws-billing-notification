venv:
	python -m venv slsvenv

activate:
	source ./slsvenv/bin/activate

deploy:
	sls deploy --aws-profile $(PROFILE)

pip_install:
	pip install -r requirements.txt

pip_freeze:
	pip freeze > requirements.txt
