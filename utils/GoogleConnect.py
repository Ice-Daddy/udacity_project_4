from google_auth_oauthlib.flow import Flow
from flask import make_response
import json
from httplib2 import Http


class GConnect():
    """Handles OAuth Connection via Google"""

    def __init__(
        self,
        session,
        json_path="config/client_secrets.json"
    ):
        """"""

        self.json_path = json_path
        self.session = session
        self.CLIENT_ID = json.loads(open(
            json_path, "r").read())["web"]["client_id"]
        self.access_token = ""
        self.gplus_id = ""
        self.data = ""

    def gconnect(self, data):
        self.ask_Google_for_user_data(data)
        self.compare_credentials()

    def ask_Google_for_user_data(self, data):
        info_url = "https://www.googleapis.com/userinfo/v2/me"
        flow = Flow.from_client_secrets_file(
            self.json_path,
            scopes=['profile', 'email'],
            redirect_uri='http://localhost:5000/gconnect'
        )

        self.access_token = flow.fetch_token(code=data)["access_token"]
        session = flow.authorized_session()
        self.data = session.get(info_url).json()
        self.gplus_id = self.data["id"]

    def compare_credentials(self):
        url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="
        url = "{}{}".format(url, self.access_token)
        result = json.loads(self.send_token_to_google(url)[1])
        stored_access_token = self.session.get("access_token")
        stored_gplus_id = self.session.get("gplus_id")

        if result.get("error") is not None:
            self.dump_runtime_error(
                result["error"], 500)

        if result["user_id"] != self.gplus_id:
            self.dump_runtime_error(
                "Token's user ID doesn't match given user ID.", 401)

        if result["issued_to"] != self.CLIENT_ID:
            self.dump_runtime_error(
                "Token's client ID does not match app's.", 401)

        if stored_access_token is not None\
                and self.gplus_id == stored_gplus_id:
            self.dump_runtime_error(
                "Current user is already connected.", 200)

    def send_token_to_google(self, url):
        h = Http()
        return h.request(url, "GET")

    def dump_runtime_error(self, error_message, error_number):
        response = make_response(json.dumps(
            error_message, error_number
        ))
        response.headers["Content-Type"] = "application/json"
        self.response = response
        raise RuntimeError

    def gdisconnect(self, access_token):
        if access_token is None:
            self.dump_runtime_error(
                "Current User is not logged in", 403
            )
        googleapi_url = "https://accounts.google.com/o/oauth2/revoke?token="
        url = "{}{}".format(googleapi_url, access_token)
        results = self.send_token_to_google(url)[0]
        if results["status"] == "200":
            return True
        else:
            self.dump_runtime_error(
                "Failed to revoke token for given user", 400
            )
            return False
