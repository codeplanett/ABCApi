import json

import cryptography.fernet
import cryptography.utils

from config import FERNET_KEY


_FERNET = cryptography.fernet.Fernet(str(FERNET_KEY))


def encrypt_json(data):
    return _FERNET.encrypt(json.dumps(data).encode('utf-8'))


def decrypt_json(data):
    try:
        return json.loads(json.loads(_FERNET.decrypt(data).decode('utf-8')))
    except TypeError:
        return json.loads(_FERNET.decrypt(data).decode('utf-8'))
