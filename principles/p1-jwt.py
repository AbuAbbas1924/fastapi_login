import jwt

MY_KEY = "nahdah"

msg = {"msg": "hallo"}
print("msg", msg)
encoded = jwt.encode(msg, MY_KEY, algorithm="HS256")
print("encoded", encoded)
decoded = jwt.decode(encoded, MY_KEY, algorithms="HS256")
print("decoded", decoded)
