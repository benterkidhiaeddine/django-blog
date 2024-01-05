# Installation

1. First install pipenv in your global python installation if you don't have it

```
pip install pipenv --user

```

2. run the following command to start a virtualenv and install dependencies

```
pipenv install

```

3. run the virtual environment of pipenv

```
pipenv shell

```

4.  cd into the directory of the project and run the migrations to create the database

```
cd blogsite
python manage.py migrate

```

5. setup and .env file inside the blogsite project directory and put inside it the credentials for you amazon simple email service like so

```
AWS_SES_ACCESS_KEY_ID=aws-ses-access-id
AWS_SES_SECRET_ACCESS_KEY=aws-ses-secret-access-key
```

6. Once that setup you can run the development server with

```
python manage.py runserver
```

## A note about Amazone Simple Email service

1.  To setup this service you need to first have an amazon account preferably logged in not as a Root User
2.  Go to the Amazon simple email service then verified identities under the Configuration Tab and click on create and identity
3.  Select your identity type either domain or your email ( for simple development purposes) , add it and then click "Create identity"
4.  Confirm your identity via clicking on a link that comes to your mail
5.  Setup your SMTP credentials under "SMTP" setting tab and register the .csv that has your credentials it will contain your AWS_SES_KEY_ID and AWS_SES_SECRET_KEY
6.  Go to your IAM tab in AWS services and enter to your new smtp user defined in the previous step
7.  Click on add permissions and add "AmazonSESFullAccess" to this user
8.  Once that done make sure that inside setting.py , the SES region name and region endpoint match what is mentions in your amazon account SES

Note: That this will not be usable in production as you can only send mail only to identities defined and verified inside the SES service
For production access check the following link https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html
and on more documentation about the python package used to connect to Amazon SES check : https://github.com/django-ses/django-ses
