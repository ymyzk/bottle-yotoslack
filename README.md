# bottle-yotoslack

[![Requirements Status](https://requires.io/github/ymyzk/bottle-yotoslack/requirements.svg?branch=master)](https://requires.io/github/ymyzk/bottle-yotoslack/requirements/?branch=master)

Send notifications to Slack when you received Yo!

## Requirements
* Python 2.7+ or 3.2+
* `requirements.txt`

## Configuration
### A: Use environment variables (Recommended)
* Set environment variables
  * `YOTOSLACK_YO_CALLBACK_URL`
  * `YOTOSLACK_SLACK_CHANNEL`
  * `YOTOSLACK_SLACK_URL`

### B: Use app.conf
* Copy `app.example.conf` to `app.conf`
* Edit `app.conf`

## Run
### A: Debug
* `pip install -r requirements.txt`
* Configure (add `app.conf` or set environment variables)
* `./app.py`

### B: Production
Use uWSGI or Gunicorn.

### C: Docker (Debug)
```bash
docker pull ymyzk/bottle-yotoslack
docker run -d -p 80:8080 --name my-bottle-yotoslack \
  -e YOTOSLACK_YO_CALLBACK_URL=/callback \
  -e YOTOSLACK_SLACK_CHANNEL=#yo \
  -e YOTOSLACK_SLACK_URL=https://hooks.slack.com/services/ \
  ymyzk/bottle-yotoslack
```

### D: Docker (Production w/ uWSGI)
```bash
docker pull ymyzk/bottle-yotoslack:uwsgi
docker run -d -p 80:8080 --name my-bottle-yotoslack \
  -e YOTOSLACK_YO_CALLBACK_URL=/callback \
  -e YOTOSLACK_SLACK_CHANNEL=#yo \
  -e YOTOSLACK_SLACK_URL=https://hooks.slack.com/services/ \
  ymyzk/bottle-yotoslack:uwsgi
```
