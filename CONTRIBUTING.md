# Contributing to wh0share

Thank you for considering contributing to wh0share! This guide ensures consistent code style and proper use of UV.

## What is UV?

UV is a Python-based task runner that ensures consistent script execution and code quality across contributors without virtual environments.

## Using UV

All contributions must use UV to run scripts, format code, and perform linting.

### Install UV from official repositories

- **Debian/Ubuntu:**

```bash
sudo apt update
sudo apt install uv
```

- **Arch Linux/Manjaro:**

```bash
sudo pacman -S uv
```

- **Windows:**

```bash
winget install uv
```

- **macOS:**

```bash
brew install uv
```

### Format and Lint

Before committing, run:

```bash
uv run --only-group lint black .
uv run --only-group lint isort .
uv run --only-group lint ruff check . --fix
```

> There is a pre-commit hook set up to run UV scripts automatically before each commit. Optionally, you can run them manually as shown above or using the `format.sh` script.

## Making Changes

When making changes, ensure you add the new dependencies to the corresponding group in `pyproject.toml` with:

```bash
uv add <package-name> --group <group-name>
```

Also update the `requirements.txt` file for easier installation of dependencies in Docker with:

```bash
uv export --no-hashes --no-header --no-annotate --no-dev --format requirements.txt > requirements.txt
```

## Running the Application

Use Docker Compose to run and test your changes:

```bash
docker-compose build --no-cache
docker-compose up -d
```

## Contribution Guidelines

- **Python >= 3.14** recommended
- Follow **PEP 8** style guidelines
- Respect the project structure (`app.py`, `templates/`, `static/`, `uploads/`)
- Use `secure_filename` for uploaded files
- The `uploads` folder must exist before running
- `.env` optional, only needed for custom paths or port
- Ensure code passes linting and formatting rules
- Test file uploads and downloads locally

## Submitting a Pull Request

1. Fork the repository
2. Create a new branch for your feature/fix
3. Make your changes
4. Run UV scripts before submitting (optional if pre-commit is active)
5. Test with Docker Compose
6. Submit a PR with a clear description

## Issue Reporting

Please report issues via the GitHub Issues page. Include:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Any relevant logs or screenshots
