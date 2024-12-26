import jwt
import requests
import json
from jwt.algorithms import RSAAlgorithm
import os


def decodeJWT(token: str) -> dict:
    try:
        # Request the JWKS
        url = 'https://auth-nonprod.thomsonreuters.com/.well-known/jwks.json'
        audience = 'faa81312-b677-405b-bd16-9381a2a6a845'
        # url = os.environ["JWT_URL"]
        # audience =os.environ["JWT_AUDIENCE"]
        response = requests.get(url)
        jwks = response.json()

        # Extract the public key
        key_data = jwks["keys"][0]  # Assuming the key is the first in the list
        public_key = RSAAlgorithm.from_jwk(key_data)

        decoded_token = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=audience  # os.environ["JWT_AUDIENCE"]
        )
        return decoded_token
    except Exception as e:
        print(e)
        return {}
