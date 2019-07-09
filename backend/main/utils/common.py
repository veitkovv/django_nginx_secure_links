from datetime import datetime
import re
import math


def get_link_deadline(link):
    """Берет из строки (URL) число в конце (timestamp) и переводит в datetime"""
    return datetime.fromtimestamp(int(re.search(r'[0-9]+$', str(link)).group(0)))


def sizeof_fmt(num, suffix='B'):
    """Рассчет байтов в читаемый вид"""
    if num > 0:
        magnitude = int(math.floor(math.log(num, 1024)))
        val = num / math.pow(1024, magnitude)
        if magnitude > 7:
            return '{:.1f} {}{}'.format(val, 'Yi', suffix)
        return '{:3.1f} {}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)
    return '0 байт'
