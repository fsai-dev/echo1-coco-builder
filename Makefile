build:
	poetry export -f requirements.txt > requirements.txt
	poetry build

test:
	poetry run pytest -s  --disable-warnings

publish:
	poetry publish

