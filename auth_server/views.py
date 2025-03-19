# auth_server/views.py
def oidc_userinfo(claims, user):
    # Si el usuario tiene nombre completo definido, úsalo; de lo contrario, usa user.username.
    claims['preferred_username'] = user.get_full_name() or user.username
    claims['email'] = user.email
    return claims
