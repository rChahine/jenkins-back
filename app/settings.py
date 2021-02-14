from starlette.config import Config
from starlette.datastructures import Secret

config = Config('.env')

DATABASE_URL = config('DATABASE_URL')
JWT_SECRET = config('JWT_SECRET', cast=Secret)
TESTING = config('TESTING', cast=bool, default=False)
