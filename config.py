from dotenv import load_dotenv  # to use .env
import os  # read from os


class Config:
    """ config class for environment dependencies """

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)  # this cause .env is a part of os system variables
    SECRET_KEY = os.environ.get("SECRET_KEY")
    

