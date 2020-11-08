# Test python pour devs

Ce test a pour but d'évaluer la qualité de votre code pour un objectif simple.
L'objectif est de coder une fonction POST qui reçois de la donnée utilisateur et qui insérer en base de données et une fonction Get qui récupère l'utilisateur inséré
Votre code doit inclure le nécessaire pour qu'il soit testable

## Install Nodemon for livereload
```shell script
npm i -g nodemon
```

## Run locally with virtual env
Create a virtual env
```shell script
$ pip install virtualenv
$ virtualenv --python=python3.8 venv
$ source venv/bin/activate
(venv) $ pip install --upgrade -r requirements.txt
```

## Tests unitaires via pytest
```python
python3.8 -m pytest
```

## SWAGGER / Spécifications
http://localhost:8081/api/docs

## Delivery
Faire un git repository privé (github) de votre projet et inviter https://github.com/kimi75 à ce projet
Deadline: Lundi 09/11 à 10H00
# test-poto
