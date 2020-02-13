# Installation instructions

1. Create a virtualenv with python 3.7 (not tested with other versions of
 python 3 but probably it will work)

1. Clone this repository

1. Activate the virtualenv created

1. Run

   ``` $ pip install -r requirements.txt ```

1. Run

   ``` $ python manage.py migrate ```

1. Run

   ``` $ python manage.py runserver ```
   
   In a local instalation the api may be in `http://localhost:8000/usersdata/`

## API test

You can test the api using, for example, [httpie](https://httpie.org/) or
 `curl`.

Some test examples with `httpie`:

``` $ http POST http://localhost:8000/usersdata/ age=30 dependents=0 house:='{"ownership_status": "mortgaged"}' income=100000 marital_status="single" risk_questions:='[0, 1, 0]' vehicle:='{"year": 2010}' ```

``` $ http POST http://localhost:8000/usersdata/ age=67 dependents=0 house:='{}' income=100000 marital_status="single" risk_questions:='[0, 1, 0]' vehicle:='{"year": 2010}' ```

``` $ http POST http://localhost:8000/usersdata/ age=30 dependents=0 house:='{"ownership_status": "mortgaged"}' income=100000 marital_status="married" risk_questions:='[0, 1, 0]' vehicle:='{}' ```
