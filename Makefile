run-example:
	pip3 install -e .
	python3 example/main.py

test:
	clear && printf '\e[3J'
	python3 -m unittest schubertpy/testcases/*.py

coverage:
	clear && printf '\e[3J'
	python3 -m coverage run -m unittest schubertpy/testcases/*.py
	python -m coverage report
	python -m coverage html

publish:
	rm -rf dist
	rm -rf build
	rm -rf schulze.egg-info
	bump2version --allow-dirty patch
	# pipreqs --force ./
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --verbose dist/*

uml:
	pyreverse -o dot --filter-mode ALL -k --verbose -p schubertpy .
	dot2tex classes_schubertpy.dot -t raw > mygraph.tex
	cat mygraph.tex

uml-detail:
	pyreverse -o pdf --filter-mode ALL --verbose -p schubertpy .