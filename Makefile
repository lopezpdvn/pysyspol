GITHUB_REMOTE	=	origin
GITHUB_PUSH_BRANCHS	=	master
MODULE_ROOT	=	pysyspol

.PHONY: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test         Run unit tests"

test:
	python -m unittest discover -v -s $(MODULE_ROOT)/tests/ -p test_*

push:
	git push $(GITHUB_REMOTE) $(GITHUB_PUSH_BRANCHS)
