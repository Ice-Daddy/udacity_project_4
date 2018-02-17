from oauth2client.client import\
    flow_from_clientsecrets, FlowExchangeError
from flask import make_response
import json
from requests import get
from httplib2 import Http


class GConnect():
    """Handles OAuth Connection via Google"""

    def __init__(
        self,
        session,
        json_path='config/client_secrets.json',
        welcome_path='../templates/welcome.html',
    ):
        """"""
        self.login_session = session
        self.client_secrets_json = json_path
        self.CLIENT_ID = json.loads(open(
            json_path, 'r').read())['web']['client_id']
        self.access_token = ''
        self.gplus_id = ''

    def gconnect(self, request):
        self.validate_state(request.args.get('state'))
        cred = self.create_credentials(request.data)
        self.access_token = cred.access_token
        self.gplus_id = cred.id_token['sub']
        self.compare_credentials(self.access_token, self.gplus_id)

    def gdisconnect(self, access_token):
        if access_token is None:
            self.dump_runtime_error(
                'Current User is not logged in', 401
            )
        results = self.check_credentials_at_google(
            'https://accounts.google.com/o/oauth2/revoke?token='
        )[0]
        if results['status'] == 200:
            self.dump_runtime_error(
                'Successfully logged out', 200
            )
            return True
        else:
            self.dump_runtime_error(
                'Failed to revoke token for given user', 400
            )
            return False

    def validate_state(self, state):
        """Validates that the state token sent with login is
        the same that was generated"""
        if state != self.session['state']:
            self.dump_runtime_error(
                'Invalid state parameter', 401)

    def create_credentials(self, code):
        try:
            oauth_flow = flow_from_clientsecrets(
                self.client_secrets_json, scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(code)
        except FlowExchangeError:
            self.dump_runtime_error(
                'Failed to upgrade the authorization code.', 401)
        else:
            return credentials

    def compare_credentials(self):
        result = json.loads(
            self.check_credentials_at_google(
                'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='
            )[1]
        )
        stored_access_token = self.session.get('access_token')
        stored_gplus_id = self.session.get('gplus_id')

        if result.get('error') is not None:
            self.dump_runtime_error(
                result['error'], 500)

        if result['user_id'] != self.gplus_id:
            self.dump_runtime_error(
                "Token's user ID doesn't match given user ID.", 401)

        if result['issued_to'] != self.CLIENT_ID:
            self.dump_runtime_error(
                "Token's client ID does not match app's.", 401)

        if stored_access_token is not None\
                and self.gplus_id == stored_gplus_id:
            self.dump_runtime_error(
                "Current user is already connected.", 200)

    def get_user_data_from_google(self):
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': self.access_token, 'alt': 'json'}
        answer = get(userinfo_url, params=params)
        return answer.json()

    def check_credentials_at_google(self, url):
        url = '{}{}'.format(url, self.access_token)
        h = Http()
        return h.request(url, 'GET')

    @staticmethod
    def dump_runtime_error(error_message, error_number):
        response = make_response(json.dumps(
            error_message, error_number
        ))
        response.headers['Content-Type'] = 'application/json'
        raise RuntimeError(response)
