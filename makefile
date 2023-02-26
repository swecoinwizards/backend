LINTER = flake8
SERVER_DIR = server
DB_DIR = db
REQ_DIR = .
PYTESTFLAGS = -vv --verbose --tb=short

FORCE:

prod: all_tests github

github: FORCE
	- git commit -a
	git push origin master

all_tests: FORCE
	cd $(DB_DIR);  make tests
	cd $(SERVER_DIR); make tests

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

all_docs: FORCE
	cd $(SERVER_DIR); make docs
	cd $(DB_DIR); make docs
