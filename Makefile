dev:
	docker-compose up -d

dev-down:
	docker-compose down

push-migration:
	alembic upgrade head

start-server:
	uvicorn app.main:app --reload

install-modules:
	pip install fastapi[all] passlib[bcrypt] alembic SQLAlchemy psycopg2 pydantic-settings python-jose cryptography