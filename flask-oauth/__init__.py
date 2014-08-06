from flask import Flask, request, redirect
from .config import CLIENT_ID, CLIENT_SECRET
import urllib
import simplejson as json
import logging

# CONF
THIRD_PARTY_AUTH_ENDPOINT = 'https://github.com/login/oauth/authorize'
THIRD_PARTY_ACCESS_TOKEN_ENDPOINT = 'https://github.com/login/oauth/access_token'
THIRD_PARTY_API_ENDPOINT = 'https://api.github.com/user'

# APP
REMOTE_USER = None
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    global REMOTE_USER
    # If already logged in
    if REMOTE_USER:
        return '<p>You are logged in as {}</p> <p><a href="/logoff">Log off</a>.</p>'.format(REMOTE_USER)

    # We are in the log in process
    elif request.args.get('code'):
        # Exchange code for an access_token
        data = {
            'code': request.args.get('code'),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        enc_data = urllib.parse.urlencode(data)
        enc_data = bytes(enc_data, 'utf-8')
        LOGGER.info("ENC DATA: {}".format(enc_data))
        gh_resp = urllib.request.urlopen(THIRD_PARTY_ACCESS_TOKEN_ENDPOINT, data=enc_data)
        gh_resp_qs = urllib.parse.parse_qs(gh_resp.read())
        LOGGER.info("GH RESP QS: {}".format(gh_resp_qs))
        access_token = gh_resp_qs[b'access_token'][0].decode('utf-8')
        LOGGER.info("ACCESS TOKEN: {}".format(access_token))

        # Exchange access_token for user id.
        gh_resp_id = urllib.request.urlopen('{api_url}?access_token={at}'
                                            .format(api_url=THIRD_PARTY_API_ENDPOINT, at=access_token))
        gh_resp_id = gh_resp_id.read().decode('utf-8')
        LOGGER.info("GH RESP ID: {}".format(gh_resp_id))
        resp_id_dec = json.loads(gh_resp_id)
        LOGGER.info("GH RESP ID JSON DEC: {}".format(resp_id_dec))
        REMOTE_USER = resp_id_dec['id']
        LOGGER.info('REMOTE USER: {}'.format(REMOTE_USER))

        return redirect('/')

    # Not logged in nor in the process of
    else:
        return 'Please <a href="{auth_endpoint}?client_id={cid}">log in</a>.'\
            .format(auth_endpoint=THIRD_PARTY_AUTH_ENDPOINT, cid=CLIENT_ID)

@app.route('/logoff')
def logoff():
    global REMOTE_USER
    REMOTE_USER = None
    return redirect('/')

if __name__ == '__main__':
    app.run(port=9090)
