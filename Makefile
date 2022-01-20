build:
	rm -rf ./dist
	poetry export -f requirements.txt > requirements.txt
	poetry build

test:
	poetry run pytest -s  --disable-warnings

publish: build
	poetry publish

