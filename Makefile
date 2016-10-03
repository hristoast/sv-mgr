DESTDIR = /usr/bin

.DEFAULT_GOAL := help

help:
	@echo "\033[91m##############################"
	@echo "#"
	@echo "# SV-MGR MAKEFILE USAGE:"
	@echo "#"
	@echo "##############################\033[0m"
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Clean project workspace
	@/bin/rm -fr __pycache__

install: ## Install sv-mgr
	@echo INSTALLING SV-MGR INTO "$(DESTDIR)" NOW ...
	@ln -fs $$(pwd)/sv_mgr.py $(DESTDIR)/sv-disable
	@ln -fs $$(pwd)/sv_mgr.py $(DESTDIR)/sv-enable
	@ln -fs $$(pwd)/sv_mgr.py $(DESTDIR)/sv-mgr

test: ## Run unit tests
	@./test.py
