FROM python:3.9

RUN useradd -D -u 1001 runner
USER runner

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* ./

ENTRYPOINT ["/usr/src/app/sync-strings.py"]

