default : build

PACKAGE_FILES = dist/python-hypothesis-0.2.1.tar.gz \
                dist/python_hypothesis-0.2.1-py2-none-any.whl \
                dist/python_hypothesis-0.2.1-py3-none-any.whl

build : $(PACKAGE_FILES)

dist/python-hypothesis-0.2.1.tar.gz : 
	python setup.py sdist

dist/python_hypothesis-0.2.1-py2-none-any.whl : 
	python setup.py bdist_wheel

dist/python_hypothesis-0.2.1-py3-none-any.whl : 
	python3 setup.py bdist_wheel

register : 
	python setup.py register

upload : $(PACKAGE_FILES)
	python -m twine upload $^

check : 
	python setup.py check

test : 
	python -m unittest -vb tests

test3 : 
	python3 -m unittest -vb tests

clean : 
	rm -rf MANIFEST \
           h_annot/*.pyc \
           tests/*.pyc \
           h_annot/__pycache__ \
           tests/__pycache__

clobber : clean
	rm -rf dist

# eof
