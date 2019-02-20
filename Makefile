default : build

PACKAGE_FILES = dist/python-hypothesis-0.2.1.tar.gz \
                dist/python_hypothesis-0.2.1-py2-none-any.whl

build : $(PACKAGE_FILES)

dist/python-hypothesis-0.2.1.tar.gz : 
	python setup.py sdist

dist/python_hypothesis-0.2.1-py2-none-any.whl : 
	python setup.py bdist_wheel

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
	rm -f MANIFEST h_annot/*.pyc tests/*.pyc

clobber : clean
	rm -rf dist

# eof
