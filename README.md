# Raffles API
Yuor API for Raffles manage


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
