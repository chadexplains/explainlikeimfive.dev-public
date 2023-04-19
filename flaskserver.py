import os
from flask import Flask, request, jsonify, render_template, session, redirect, request, url_for
from flask_cors import CORS,cross_origin

from google.oauth2.credentials import Credentials

from upload_to_youtube import upload_video_to_youtube
from get_authenticated_service import get_authenticated_service
from credentials_to_dict import credentials_to_dict

app = Flask(__name__)
app.secret_key = "secret"
CORS(app)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']

    # Save the video file locally
    video_file.save('recordedVideo.mkv')
    if 'credentials' not in session:
        return redirect('/authorize')

    credentials = Credentials(session['credentials'])


    response = upload_video_to_youtube(credentials, 'recordedVideo.mkv', 'Video Title', 'Video Description', 'unlisted')

    session['credentials'] = credentials_to_dict(credentials)

    # Clean up the local video file
    video_file.close()
    os.remove('recordedVideo.webm')

    if response.status_code == 200:
        # Video uploaded successfully
        return jsonify({'status': 'success'}), 200
    else:
        # Video upload failed
        return jsonify({'error': 'Failed to upload video'}), 500


@app.route('/authorize')
def authorize():
    flow = get_authenticated_service()

     # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state =  flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
    
    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url) 

@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']
    flow = get_authenticated_service()

    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('upload_video'))






if __name__ == '__main__':
    app.run(debug=True)
