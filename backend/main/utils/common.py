from datetime import datetime
import re


def get_link_deadline(link):
    return datetime.fromtimestamp(int(re.search(r'[0-9]+$', str(link)).group(0)))
