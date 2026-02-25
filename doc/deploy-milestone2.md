# Deploy guide for milestone 2 (render)

## 1. what you need to do
- create or login to a render account
- connect render with your github account
- allow access to this repository

## 2. render settings
- service type: web service
- build command: `pip install -r requirements.txt`
- start command: `gunicorn src.app:server`
- python version: default is fine

## 3. after deploy
- open the public url and test filters and charts
- copy the public url
- paste the url at the top of `README.md`

## 4. release and canvas
- create a github release named `milestone-2`
- copy the release url
- paste it into `canvas-submission.md`
- submit the release url to canvas
