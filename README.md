## Simple FastAPI Custom CI/CD Server for Docker on Gunicorn and Uvicorn

> Please don\`t forget create `.env` file in the project directory with environment variables and change working directory in `cicdserver.service` file!

```dotenv
#~/.env
DEPLOY_TOKEN=something_secret_string
DEPLOY_HOST=0.0.0.0
DEPLOY_PORT=1234
```
