import os

from dotenv import load_dotenv

load_dotenv("./.env")

if __name__ == "__main__":
    print(os.getenv("SECRET", "no secret there"))
