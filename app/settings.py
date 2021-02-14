from starlette.config import Config
from starlette.datastructures import Secret
import os
import sys

env = os.environ['ENV_MODE']

if env is not None:

    config = Config(f'.env.{env}')

    DATABASE_URL = config('DATABASE_URL')
    JWT_SECRET = config('JWT_SECRET', cast=Secret)
    RUNNING_TEST = os.environ['RUNNING_TEST'] if not None else False

else:
    sys.exit("ENV_MODE must be set before start")
