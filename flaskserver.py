import os
from flask import Flask, request, jsonify, render_template
import requests
from upload_to_youtube import upload_video_to_youtube

app = Flask(__name__)

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
    response = upload_video_to_youtube(
        'recordedVideo.mkv', 'Video Title', 'Video Description', 'unlisted')

    # Clean up the local video file
    video_file.close()
    os.remove('recordedVideo.webm')

    if response.status_code == 200:
        # Video uploaded successfully
        return jsonify({'status': 'success'}), 200
    else:
        # Video upload failed
        return jsonify({'error': 'Failed to upload video'}), 500


if __name__ == '__main__':
    app.run(debug=True)
