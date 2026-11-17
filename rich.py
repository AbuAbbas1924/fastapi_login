from faker import Faker

fake = Faker()

print("Faker package test succeeded")
print(f"Name:    {fake.name()}")
print(f"Email:   {fake.email()}")
print(f"Address: {fake.address().replace('\n', ', ')}")
