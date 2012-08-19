# Black Hole With Small GAP #

## About ##
“Black Hole with Small Gap” (BHWSG) is SMTP server with web frontend, which is useful while your application is in development mode. SMTP server will catch all mails and will show them onto web UI, so that you can use real email addresses of real people and do not worry about boring those real people. You can debug mail content, improve HTML mail’s visual representation and make this in more natural way, using real emails, w/o chance that debug mail will be delivered to  real people.

To make development process more fun, we are try to provide full amount of tools, which can be useful, when you develop your application: you are able to see all information, regarding mail, like headers, internal representation, html/text version and so on; using rich forwarding rules, you can configure BHWSG to deliver some of emails, your application sent, which can be useful in case you use traceback.me for exceptions or similar tools; privacy settings allow you to do not worry about sensetive information, present in your mails; attachment review feature allow you to work with mail attachemnts, just like you do this in your favorite mail client.

We hope, that BHWSG will become one of your favorite development helper tool.

(__This is our plan. Not everything is done yet. If you need working solution just now, look at existing service, where we take idea and inspiration__ http://mailtrap.io)

## Prerequisites ##

- python >= 2.5
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment ###
Create a virtual python environment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv bhwsg-env
```

#### For virtualenv ####
```bash
virtualenv bhwsg-env
cd bhwsg-env
source bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone https://github.com/romanosipenko/bhwsg.git bhwsg
```

### Install requirements ###
```bash
cd bhwsg
pip install -r contrib/requirements.pip
```

### Configure project ###
```bash
cp src/bhwsg/settings_local.py.example src/bhwsg/settings_local.py
vi src/bhwsg/settings_local.py
```

### Sync database ###
```bash
cd src
python manage.py syncdb
python manage.py migrate
```

### Setup and run celery ###
```bash
cd src
python manage.py celeryd
```

## Running ##
```bash
python manage.py runserver
```
Open browser to http://127.0.0.1:8000
