import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'nsndvd.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'nsndvd-ucs-api'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
DONE implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        raise AuthError({
            'code': 'auth_header_missing',
            'description': 'Authorization header missing.'
        }, 401)

    if auth_header.split()[0].lower() != 'bearer' or len(auth_header.split()) != 2:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorization header must be in "bearer" token format.'
        }, 401)

    return auth_header.split()[1]

'''
DONE implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if not payload['permissions']:
        raise AuthError({
            'code': 'no_permissions_in_payoload',
            'description': 'Authorization token doesn\'t contain permissions payload'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'user_not_allowed',
            'description': 'The user doesn\'t have the required permission'
        }, 403)
    
    return True

'''
DONE implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    our_key = {}
    well_known_jwks_url = urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    # print('\n')
    # print(well_known_jwks_url)
    jwks = json.loads(well_known_jwks_url.read())
    # print('\n')
    # print(jwks)
    # print('\n')
    # print(token)
    # print('\n')

    header = jwt.get_unverified_header(token)
    # print('header: ' + repr(header))
    # print('\n')
    if 'kid' not in header:
        raise AuthError({
            'code': 'invalid_authentication_header',
            'description': 'Missing kid in token.'
        }, 401)

    # Find the key with the same kid of our header among the ones we received in jwks
    for key in jwks['keys']:
        if key['kid'] == header['kid']:
            our_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if not our_key:
        raise AuthError({
                'code': 'invalid_header',
                'description': 'Couldn\'t find a key with the right key id.'
            }, 400)
    try:
        decoded_payload = jwt.decode(
            token,
            our_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer='https://' + AUTH0_DOMAIN + '/'
        )

        return decoded_payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)
    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Please, check the audience and issuer.'
        }, 401)
    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)
    
'''
WAS DONE ALREADY implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as err:
                # print(err)
                abort(err.status_code, err.error['description'])
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator