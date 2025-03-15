from dotenv import dotenv_values

env = dotenv_values()

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = "HS256"
DATABASE_URL = env["DATABASE_URL"]
