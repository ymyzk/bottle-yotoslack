FROM ymyzk/bottle-yotoslack

RUN apt-get update \
        && apt-get install -y --no-install-recommends \
            gcc \
            libc6-dev \
        && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.uwsgi.txt

ENTRYPOINT ["uwsgi", "uwsgi.ini"]
