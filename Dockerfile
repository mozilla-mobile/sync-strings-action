FROM python:3.9


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* ./

RUN useradd -D -u 1001 runner
USER runner

ENTRYPOINT ["/usr/src/app/sync-strings.py"]

