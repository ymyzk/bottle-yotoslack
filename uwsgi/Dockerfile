FROM ymyzk/bottle-yotoslack

RUN apt-get update \
        && apt-get install -y --no-install-recommends build-essential \
        && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.uwsgi.txt

ENTRYPOINT ["uwsgi", "uwsgi.ini"]
