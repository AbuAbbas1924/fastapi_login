import os

if __name__ == "__main__":
    print(os.getenv("SECRET", "no secret there"))
