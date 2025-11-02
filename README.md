# wh0share

A simple LAN file-sharing service with a web interface, Dockerized for easy deployment.

## Features

- Upload, view, and download files through a web interface
- Files are stored on the host machine (persistent)
- Configurable via `.env` (optional)
- Ready to run with Docker and Docker Compose

## Setup

1. Clone the repository:

```bash
git clone https://github.com/wh0crypt/wh0share.git
cd wh0share
```

2. Create the uploads directory on the host:

```bash
mkdir -p uploads
sudo chown -R $USER:$USER uploads
```

> Ensure the `uploads` directory has appropriate permissions for Docker to read/write files. If you plan to use a different directory for uploads, create that directory instead and adjust the `.env` file accordingly.

3. Configure `.env` (optional):

```bash
SECRET_KEY="supersecretkey"
SITE_INDEX="/srv/wh0share"
UPLOAD_FOLDER="/srv/wh0share/uploads"
HOST_PORT="8000"
DEBUG="False"
ALLOWED_EXTENSIONS="txt,pdf,png,jpg,jpeg,gif"
MAX_CONTENT_LENGTH_MB="1024"    # default 1 GB
MAX_TOTAL_STORAGE_MB="10240"    # default 10 GB
```

> You do not need a `.env` file if you are okay with the default uploads directory inside the project and default port `8000`. The `.env` is only necessary if you want files stored in a different directory or to change the exposed port. Check the `.env.example` for reference.

4. Build and run with Docker Compose:

```bash
docker-compose build --no-cache
docker-compose up -d
```

4. [Optionally] Run the application without Docker and Docker Compose:

```bash
uv run gunicorn -b 0.0.0.0:8000 app:app
```

5. Access the app:

- **Local:** [http://localhost:8000](http://localhost:8000)
- **Remote:** [http://<SERVER_IP>:8000](http://<SERVER_IP>:8000)

> Make sure port `8000` (or the port you set in `HOST_PORT`) is open in your firewall settings.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! For more details, please see [CONTRIBUTING.md](CONTRIBUTING.md).
