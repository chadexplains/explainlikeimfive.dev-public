let recorder; // Global variable to store the recorder instance
const STREAM_TIME = 10000;
function startRecording() {
    navigator.mediaDevices.getDisplayMedia({ video: true}) // Capture screen
    .then(async (displayStream) => {

        // If display surface is not monitor, it means user chose something other than entire screen
        let chromiumdisplaySurface = displayStream.getVideoTracks()[0].getSettings().displaySurface;
        let firefoxdisplaySurface = displayStream.getVideoTracks()[0].label;

        // Check for Chrome
        if (navigator.userAgent.includes('Chrome') && chromiumdisplaySurface !== "monitor") {
            displayStream.getVideoTracks().forEach(track => track.stop());
            throw 'Selection of entire screen mandatory!';
        }

        // Check for Firefox
        else if (navigator.userAgent.includes('Firefox') && firefoxdisplaySurface !== 'Primary Monitor'){
            displayStream.getVideoTracks().forEach(track => track.stop());
            throw 'Selection of entire screen mandatory!';
        }


        [videoTrack] = displayStream.getVideoTracks();
        const audioStream = await navigator.mediaDevices.getUserMedia({audio: true}).catch(e => {throw e});
        [audioTrack] = audioStream.getAudioTracks();
        stream = new MediaStream([videoTrack, audioTrack]);
        recorder = RecordRTC(stream, { type: 'video' }); // Create a recorder instance
        recorder.startRecording(); // Start recording

        setTimeout(()=>{stopRecording(); stream.stop();} , STREAM_TIME);
    })
    .catch(function (error) {
        alert('Error accessing screen. Please set permissions to view Entire Screen');
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

