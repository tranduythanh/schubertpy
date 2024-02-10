test:
	clear && printf '\e[3J'
	python3 -m unittest testcases/*.py

coverage:
	clear && printf '\e[3J'
	python3 -m coverage run -m unittest testcases/*.py
	python -m coverage report
	python -m coverage html