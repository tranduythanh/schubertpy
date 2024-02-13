test:
	clear && printf '\e[3J'
	python3 -m unittest testcases/*.py

coverage:
	clear && printf '\e[3J'
	python3 -m coverage run -m unittest testcases/*.py
	python -m coverage report
	python -m coverage html

publish:
	rm -rf dist
	rm -rf build
	rm -rf schulze.egg-info
	pipreqs --force ./
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*