# Cria um ambiente onde a build possa ocorrer.
FROM debian:buster-slim AS build
RUN apt-get update && \
  apt-get install -y curl && \
  curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
  mkdir -p /usr/share/man/man1 && \
  apt-get install --no-install-suggests --no-install-recommends -y \
  gcc \
  make \
  python3-venv \
  libpython3-dev \
  libmariadb-dev \
  nodejs && \
  python3 -m venv /venv && \
  /venv/bin/pip install -U pip

# Constói o venv.
FROM build AS python-build-env
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt

# Instala e comprime as dependências estáticas.
FROM python-build-env AS nodejs-build-env
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
COPY manage.py /app/manage.py
COPY Makefile /app/Makefile
COPY visprof/*.py /app/visprof/
COPY visprof/templates /app/visprof/templates/
COPY visprof/static /app/visprof/static/
WORKDIR /app
RUN npm i && PYTHON=/venv/bin/python make static

# Copia todos os ficheiros necessários para imagem final.
# FROM gcr.io/distroless/python3-debian10:debug
FROM debian:buster-slim
RUN apt-get update && \
  apt-get install --no-install-suggests --no-install-recommends -y \
  python3-venv \
  libmariadb-dev
COPY --from=python-build-env /venv /venv/
COPY --from=nodejs-build-env /static /static/
COPY manage.py /app/manage.py
COPY visprof/*.py /app/visprof/
COPY visprof/templates /app/visprof/templates/
WORKDIR /app
ENTRYPOINT ["/venv/bin/gunicorn", "-b", "0.0.0.0:8081", "-w", "4", "visprof.wsgi"]

# docker build . --tag visprof
# LINUX: docker run --rm --env-file=./.env.prod --network=host --name=visprof test
# MAC: docker run --rm --env-file=./.env.prod --publish=8081:8081 --name=visprof test
# docker run --entrypoint=bash -it --name=visprof test
