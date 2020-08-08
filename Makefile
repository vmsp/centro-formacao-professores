PYTHON ?= python3

DUMMY_ENV := \
	SECRET_KEY=build-static \
	DATABASE_URL=mysql://localhost \
	EMAIL_URL=smtp://localhost \
	DEFAULT_FROM_EMAIL= \
	DEBUG=off \
	STATIC_ROOT=/static

static:
	$(DUMMY_ENV) $(PYTHON) manage.py compress -f
	$(DUMMY_ENV) $(PYTHON) manage.py collectstatic \
		-i '*.txt' \
		-i bootstrap \
		-i ckeditor4 \
		-i django_extensions \
		-i django_tables2 \
		-i jquery \
		-i js-cookie \
		-i popper.js \
		-i 'visprof/*.js' \
		-i 'visprof/*.css' \
		--noinput

tests:
	./manage.py test -p '*_test.py'

image:
	docker build . --tag visprof

deps: requirements.txt requirements_dev.txt
	pip-sync $^

requirements.txt: requirements.in
	pip-compile $<

requirements_dev.txt: requirements_dev.in
	pip-compile $<

.PHONY: static tests image deps
