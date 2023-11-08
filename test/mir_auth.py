import base64

username = "distributor"
password = "distributor"

credentials = f"{username}:{password}"
credentials_encoded = base64.b64encode(credentials.encode()).decode("utf-8")

auth_header = f"Basic {credentials_encoded}"

print(auth_header)
