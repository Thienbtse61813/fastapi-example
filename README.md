# Fastapi-Example

REST API service to learn how to use FastAPI with SQLAlchemy and PostGreSQL

## Setup

### 1. Docker compose is used to run the service.

- Add the following environment variables to your `docker-compose.yml` file:

```yaml
DB_HOST=db
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
```

- Configure `app/.env` file by creating a copy from `app/.env.sample`

```bash
DEFAULT_PASSWORD=your_default_password_for_init_admin
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

```

- Run the service

```bash
docker compose up -d --build
```

### 2. Run with uvicorn

- Create a virtual environment using `virtualenv` module in python.

```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```

- Configure `app/.env` file by creating a copy from `app/.env.sample`

```bash
ASYNC_DB_ENGINE=postgresql+asyncpg
DB_ENGINE=postgresql
DB_HOST=localhost
DB_USERNAME=postgres
DB_PASSWORD=123456
DB_NAME=fastapi_assignment

DEFAULT_PASSWORD=your_default_password_for_init_admin
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

```

- Setup a postgres docker container

```bash
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=<your-preferred-one> -d postgres:14
```

- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible.

```bash
# Migrate to latest revison
alembic upgrade head

# Dowgragde to specific revision
alembic downgrade <revision_number>

# Downgrade to base (revert all revisions)
alembic downgrade base
```

- Run the service

```bash
uvicorn app.main:app --reload
```
