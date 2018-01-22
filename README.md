# TIM - The infos maschine (CMS)

Hier wird ein CMS für den 1LIVE Infosbot entwickelt.

## Getting started

### Running locally

We recommend using the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) to run the webserver

For a better experience while developing use this `.env` file: (Don't use in production)

```bash
DEBUG=True
GUNICORN_CMD_ARGS="--reload -k eventlet"
```

Then run:

```bash
pipenv run heroku local
```
