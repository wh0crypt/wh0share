uv run --only-group lint black .
uv run --only-group lint isort .
uv run --only-group lint ruff check . --fix
