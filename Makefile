GITHUB_REMOTE	=	origin
GITHUB_PUSH_BRANCHS	=	master
MODULE_ROOT	=	pysyspol

.PHONY: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  test         Run unit tests"
	@echo "  push         Push branches to main remote"
	@echo "  clean        Clean cache and optimized code"

test:
	python -m unittest discover -v -s $(MODULE_ROOT)/tests/ -p test_*

push:
	git push $(GITHUB_REMOTE) $(GITHUB_PUSH_BRANCHS)

clean:
	@rm -rvf $(MODULE_ROOT)/__pycache__
	@find . -iname '*pyc' -print0 | xargs -0 rm -rvf
