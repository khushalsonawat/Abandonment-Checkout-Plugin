This project has been divided into 2 section:
1. Frontend
2. Backend

To run the project locally, follow the following steps

First clone this repository into your local system

#### Frontend

`cd frontend && npm install`

`ng serve`

### Backend

Create a virtual environment with the following command and activate the same

`python -m venv env`

For windows

`env\Scripts\activate`

For Ubuntu

`source env/bin/activate`

Then

`cd backend && pip install -r requirements.txt`

You will need to create a .env file where you can store your API_KEY, SECRET_KEY and SHARED_SECRET_KEY that you get from your Partner's Dashboard. I have added a .env.example file for reference. Once these are done

`python manage.py migrate`

You will need separate terminals for running celery and celery-beat

For running celery

`celery -A backend worker --pool=solo -l INFO`

For running celery-beat

`celery -A backend beat -l INFO`

And run the local server in a separate terminal

`python manage.py runserver`

You will have to subscribe to 3 different webhooks, namely create_cart, update_cart and order_create from Shopify admin panel.

Also note that shopify only accepts https:// URL for subscribing to webhooks. You can use a tunneling service like ngrok which can provide https URL which direct yur traffic to the local server.