import string

base = 62
alphabet = string.digits + string.ascii_letters


def encode(url_id):
    result = []
    while url_id > 0:
        val = url_id % base
        result.append(alphabet[val])
        url_id //= base
    return ''.join(result[::-1])


def decode(value):
    num = 0
    idx = 0
    val_len = len(value)
    for char in value:
        power = (val_len - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num
