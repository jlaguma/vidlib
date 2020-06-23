# VIDEO LIBRARY

Video Library web app written in Django.

## Installation


```bash
pipenv shell
pipenv install
pipenv makemigrations
pipenv migrate
```

## Usage

Note that you will need YOUTUBE_API_KEY configured in views.py file.
Setup a yotube app on console.developers.google.com to use Youtube Data API v3
and get API Key from there.

```bash
pipenv createsuperuser
./manage.py runserver
http://127.0.0.1:8000
```

## Author
[James La Guma](https://www.linkedin.com/in/jlaguma/)