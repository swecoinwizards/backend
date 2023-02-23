LINTER = flake8
TEST_DIR = tests
PYTESTFLAGS = -vv --verbose --tb=short --cov=$(PKG) --cov-branch --cov-report term-missing

FORCE:

tests: lint unit

unit: FORCE
	pytest $(PYTESTFLAGS)

lint: FORCE
	$(LINTER) *.py
	$(LINTER) $(TEST_DIR) *.py

%.py: FORCE
	pytest -s tests/test_$*.py

docs: FORCE
	pydoc3 -w ./*py
	git add *html