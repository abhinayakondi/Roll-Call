import os
import json
import requests
import google_auth_oauthlib.flow
from flask import url_for, session
from app.config import Config
from app.services.auth_service.token import credentials_to_dict, check_granted_scopes


def create_flow(state=None):
    """
    Creates the Google OAuth flow using either:
    - CLIENT_SECRETS_JSON (Render)
    - client_secrets.json file (local)
    """

    client_secrets_json = os.environ.get("CLIENT_SECRETS_JSON")

    if client_secrets_json:
        # Render / production
        client_config = json.loads(client_secrets_json)

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config,
            scopes=Config.SCOPES,
            state=state
        )
    else:
        # Local development
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            Config.CLIENT_SECRETS_FILE,
            scopes=Config.SCOPES,
            state=state
        )

    return flow


def initiate_google_auth(callback_route):
    """
    Initiates the Google OAuth flow by generating the authorization URL.
    """
    flow = create_flow()
    flow.redirect_uri = url_for(callback_route, _external=True)
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    session["state"] = state
    return authorization_url


def handle_oauth_callback(authorization_response, redirect_uri):
    """
    Exchanges the authorization code for credentials.
    """
    if "state" not in session:
        raise Exception("OAuth state is missing or invalid.")
    state = session["state"]
    flow = create_flow(state=state)
    flow.redirect_uri = redirect_uri
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    credentials_dict = credentials_to_dict(credentials)
    features = check_granted_scopes(credentials_dict)
    session["features"] = features

    return credentials_dict