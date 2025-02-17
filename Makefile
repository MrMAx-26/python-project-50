install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl --force

gendiff:
	uv run gendiff

lint:
	uv run ruff check gendiff

check:
	test check

test:
	uv run pytest
