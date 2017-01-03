"""Security."""
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from passlib.apps import custom_app_context as pwd_context


class MyRoot(object):
    """A root."""

    def __init__(self, request):
        """Init."""
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'add')
    ]


def check_credentials(username, password):
    """Check."""
    if username and password:
        if username == os.environ['AUTH_USERNAME']:
            if pwd_context.verify(password, os.environ['AUTH_PASSWORD']):
                return True
    return False


def includeme(config):
    """Security."""
    auth_secret = os.environ.get('AUTH_SECRET', 'secret')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg="sha512"
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(MyRoot)