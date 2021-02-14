from fastapi import FastAPI
from .routes import router
from .settings import TESTING
from .models import ( # noqa F401
    User, UserChoice, Choice
)

import sys

app = FastAPI(
    title="CI api",
    docs_url=None,
    redoc_url="/doc"
)

app.include_router(router, tags="main router")


if TESTING:
    sys.exit(0)
