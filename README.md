# Currency Exchange

This is a Django REST API for currency exchange rates.

## Quickstart

1. **Clone the repository:**

    ```sh
    git clone https://github.com/TeriyakiGod/currency-exchange
    cd currency-exchange
    ```

2. **Build and run the Docker containers:**

    ```sh
    docker-compose up --build
    ```

3. **Apply database migrations:**

    ```sh
    docker-compose exec app python manage.py migrate
    ```
    
4. **Collect static files:**

    ```sh
    docker-compose exec app python manage.py collectstatic --noinput
    ```

5. **Access the app:**

    Open your browser and go to `http://localhost:8000`. It should display the API documentation.

## Administration

You can add currencies and fetch exchange rates in the admin panel.

1. **Create a superuser:**

    ```sh
    docker-compose exec app python manage.py createsuperuser
    ```

2. **Access the admin panel:**

    Open your browser and go to `http://localhost:8000/admin`.

3. **Log in:**

    Use the admin credentials you set up during the initial configuration.

4. **Manage currencies:**

    Go to the Currencies section. Here you can manage the currencies.

5. **Browse and fetch exchange rates:**

    Go to the Exchange Rates section. Here u can browse historical rates.
    To fetch latest exchange rates press button in the upper right corner.


## Endpoints

- **List all currencies:**

    ```
    GET /currency/
    ```

- **Get the latest exchange rate between two currencies:**

    ```
    GET /currency/<base_currency>/<quote_currency>/
    ```

- **API schema:**

    ```
    GET /api/schema/
    ```

- **Swagger UI:**

    ```
    GET /api/schema/swagger
    ```

## Environment Variables

- **SECRET_KEY:** The secret key for the Django application.
- **DEBUG:** Set to `True` for development.
- **DEFAULT_CURRENCIES:** Comma-separated list of default currencies (e.g., `USD,EUR,JPY,PLN`).

## License

This project is licensed under the MIT License.