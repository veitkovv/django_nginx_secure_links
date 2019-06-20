import hashlib
from base64 import b64encode
from datetime import datetime, timedelta
from urllib.parse import urlparse

from django.conf import settings


def secure_link(baselink):
    """
    :param baselink: base url for signing
    :return: signed link as str
    """

    url = urlparse(baselink)
    dt_expires = datetime.now() + timedelta(seconds=settings.PUBLIC_URL_TTL)

    expires = int(dt_expires.timestamp())

    hashstring = f'{settings.NGINX_SECRET}{url.path}{expires}'

    m = hashlib.md5()
    m.update(bytes(hashstring, encoding='utf-8'))
    protection_string = b64encode(m.digest(), altchars=b'-_').replace(b'=', b'').decode("ascii")
    protected_link = f'{baselink}?md5={protection_string}&expires={expires}'.replace(" ", "%20")  # пробелы в url

    return protected_link
