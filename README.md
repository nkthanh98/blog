# My blog web application
---

Written by Django 2.1.7


### For development

```bash
$ DJANGO_SETTINGS_MODULE=myblog.dev_settings python manage.py runserver
```


### For production

```bash
$ python manage.py collectstatic 
$ gunicorn wsgi:application
```
