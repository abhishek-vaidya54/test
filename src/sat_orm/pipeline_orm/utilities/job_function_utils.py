from email.utils import parseaddr


def is_valid_group_admin(value):
    result = parseaddr(value)
    return result[1]
