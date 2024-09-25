# Web Rifas
Yuor Web Site for Raffles manage


## Deploy
1. Create a virtual environment to isolate our package dependencies locally
```
python3 -m venv venv
source env/bin/activate  # On Windows use `env\Scripts\activate
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Apply migrate
```
python manage.py migrate
```
2. We'll also create an initial user named admin with a password. We'll authenticate as that user later in our example.
```
python manage.py createsuperuser --username admin --email admin@example.com
```

### References
Token:
https://docs.djangoproject.com/en/5.0/howto/csrf/

Raffle:
https://www.youtube.com/watch?v=WcTkr-jrRIM

Rifame:
https://rifeme.com.br/ajude-me-a-ir-para-o-enj/

Sistema de Rifas:
https://www.youtube.com/watch?v=vEzBjPtRjNk

Rifei:
https://rifei.com.br/?utm_source=googleads&utm_medium=search&utm_campaign=campanhas&gad_source=1&gclid=EAIaIQobChMI08mY7KyphwMV3kVIAB3xygLSEAAYAiAAEgIJNfD_BwE