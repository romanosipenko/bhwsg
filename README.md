# Black Hole With Small GAP #
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
mkvirtualenv --no-site-packages bhwsg-env
```

#### For virtualenv ####
```bash
virtualenv --no-site-packages bhwsg-env
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
pip install -r requirements.txt
```

### Configure project ###
```bash
cp bhwsg/__local_settings.py bhwsg/local_settings.py
vi bhwsg/local_settings.py
```

### Sync database ###
```bash
python manage.py syncdb
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000
