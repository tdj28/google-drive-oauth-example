# -*- coding: utf-8 -*-
"""
This is a simple Flask app that uses Authomatic to log users in with Facebook Twitter and OpenID.
"""

from flask import Flask, render_template, request, make_response
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
#from oauth2client.client import OAuth2Credentials
import httplib2
import pprint
from apiclient.discovery import build as discovery_build
from apiclient.http import MediaFileUpload
from json import dumps as json_dumps
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage as CredentialStorage
from oauth2client.tools import run as run_oauth2

MISSING_CLIENT_SECRETS_MESSAGE = ""

OAUTH_SCOPE = ['email', 'https://www.googleapis.com/auth/drive']

REDIRECT_URI = '/'

app = Flask(__name__)

FILENAME = 'openvpn.ovpn'
CLIENT_SECRETS_FILE = 'client_secrets.json'

# File where we will store authentication credentials after acquiring them.
CREDENTIALS_FILE = 'credentials.json'

@app.route('/')
def index():
    """
    Home handler
    """
    return render_template('index.html')


@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=OAUTH_SCOPE,
                                 message=MISSING_CLIENT_SECRETS_MESSAGE)
    credential_storage = CredentialStorage(CREDENTIALS_FILE)
    credentials = run_oauth2(flow, credential_storage)
    http = httplib2.Http()
    http = credentials.authorize(http)
    drive_service = discovery_build('drive', 'v2', http=http)
    media_body = MediaFileUpload(FILENAME, mimetype='text/plain')
    body = {
                 'title': 'openvpn.ovpn',
                 'description': 'Your RJM keys',
                 'mimeType': 'text/plain'
             }

    file = drive_service.files().insert(body=body, media_body=media_body).execute()

    return render_template('index.html')
  
# Run the app.
if __name__ == '__main__':
    app.run(debug=True, port=8080)
