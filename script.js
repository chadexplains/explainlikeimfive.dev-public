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

        setTimeout(()=>{stopRecording(); stream.stop();} , 10000);
    })
    .catch(function (error) {
        console.error('Error accessing screen:', error);
    });
}

function stopRecording() {
    recorder.stopRecording(() => {
        const recordedBlob = recorder.getBlob();
        const downloadLink = document.createElement("a");
        downloadLink.href = URL.createObjectURL(recordedBlob);
        downloadLink.download = 'recordedVideo.webm';
        document.body.appendChild(downloadLink);

        downloadLink.click();

        downloadLink.parentNode.removeChild(downloadLink);
        });
        
    };
