import loginpass
from authlib.integrations import django_client


# See https://github.com/authlib/loginpass/issues/65
class Microsoft:
    NAME = 'microsoft'
    OAUTH_CONFIG = {
        'api_base_url':
            'https://graph.microsoft.com/',
        'authorize_url':
            'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
        'access_token_url':
            'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        'jwks_uri':
            'https://login.microsoftonline.com/common/discovery/v2.0/keys',
        'userinfo_endpoint':
            'https://graph.microsoft.com/oidc/userinfo',
        'client_kwargs': {
            'scope': 'openid email profile'
        },
    }


OAUTH = django_client.OAuth()

BACKENDS = [Microsoft, loginpass.Google]
