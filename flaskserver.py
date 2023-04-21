import os
from flask import Flask, request, jsonify, render_template
from simple_youtube_api.Channel import Channel

from upload_to_youtube import upload_video_to_youtube

app = Flask(__name__)
app.secret_key = "secret"

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

    channel = Channel()
    channel.login("client_secrets.json", "credentials.storage")

    upload_video_to_youtube(channel)

    # Clean up the local video file
    video_file.close()
    os.remove('recordedVideo.mkv')

    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True)