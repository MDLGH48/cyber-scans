.ONESHELL:

startup: install env run

install: env
	. env/bin/activate && pip install -r app/requirements.txt

env:
	test -d env || python3.7 -m virtualenv env;

run:
	. env/bin/activate && python app/main.py

clean_pyc:
	find . | grep -E "(__pycache__|\.pyc|.pytest_cache|.coverage|\.pyo$)" | xargs rm -rf

delete_env:
	rm -rf env;