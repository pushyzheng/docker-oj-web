import hashlib 


def get_avatar_url(email, size=300):
    hl = hashlib.md5()
    hl.update(email.encode(encoding="utf-8"))
    hash = hl.hexdigest()

    base_url = 'http://www.gravatar.com/avatar'
    avatar_url = '{}/{}?rating=g&default=identicon&size={}'.format(base_url, hash, size)

    return avatar_url