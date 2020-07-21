# song-links

## To Configure

Install virtual env

```
pip install virtualenv
```

Create an environment in your project directory

```
py -m venv venv
source venv/Scripts/activate
```

Install all necessary packages

```
pip install -r requirements.txt
```

Copy and rename .env.example to .env

```
cp .env.example .env
```

Update .env with credentials

```
source venv/Scripts/activate
export FLASK_APP="app.py"
export YT_MUSIC_KEY=""
export SPOTIFY_CLIENT_ID=""
export SPOTIFY_CLIENT_SECRET=""
export FLASK_ENV="development"
```

Source the .env

```
source .env
```

Start server

```
flask run
```

NOTE: Before committing and pushing to the repo, make sure the requirements.txt are updated with any of the imports

```
pip freeze > requirements.txt
```
