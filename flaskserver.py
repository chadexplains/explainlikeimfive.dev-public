from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']

    # Save the video file locally
    video_file.save('recordedVideo.webm')

    # Send the video file to the Loom API
    url = 'https://api.loom.com/v1/videos'
    headers = {
        'Authorization': 'Bearer YOUR_LOOM_API_TOKEN',
    }
    files = {
        'video': open('recordedVideo.webm', 'rb')
    }
    response = requests.post(url, headers=headers, files=files)

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
