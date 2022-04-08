# Ecommerce-website

## This is my Ecommerce website. Images not showing because Heroku free version.

https://khumoyunecom.herokuapp.com/


Clone repository and create **.env** file in **BASE_DIR**
```
export SECRET_KEY=Your secret_key in settings.py
export DEBUG=True
export DATABASE_URL=sqlite:///db.sqlite3
```

Install requirements in your virtual environment

```
pip install -r requirements.txt
```

and make migrations

```
python manage.py migrate
```

To adding content you should create a categories but before that, create a superuser

```
python manage.py createsuperuser
```

Then start the site

```
python manage.py runserver
```
