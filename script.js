let recorder; // Global variable to store the recorder instance

function startRecording() {
    navigator.mediaDevices.getDisplayMedia({ video: true}) // Capture screen
    .then(async (displayStream) => {
        [videoTrack] = displayStream.getVideoTracks();
        const audioStream = await navigator.mediaDevices.getUserMedia({audio: true}).catch(e => {throw e});
        [audioTrack] = audioStream.getAudioTracks();
        stream = new MediaStream([videoTrack, audioTrack]);
        recorder = RecordRTC(stream, { type: 'video' }); // Create a recorder instance
        recorder.startRecording(); // Start recording

        setTimeout(()=>{stopRecording(); stream.stop();} , 2000);
    })
    .catch(function (error) {
        console.error('Error accessing screen:', error);
    });
}

function stopRecording() {
    recorder.stopRecording(() => {
        const recordedBlob = recorder.getBlob();
        
        // Create a FormData object to send the recordedBlob as a file
        const formData = new FormData();
        formData.append('video', recordedBlob, 'recordedVideo.webm');

        // Make a POST request to your Flask API endpoint
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                console.log('Video uploaded successfully');
            } else {
                console.error('Failed to upload video');
            }
        })
        .catch(error => {
            console.error('Error uploading video:', error);
        });
    });
};

