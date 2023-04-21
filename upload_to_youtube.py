from simple_youtube_api.LocalVideo import LocalVideo
import uuid

def upload_video_to_youtube(channel):
    video = LocalVideo(file_path="recordedVideo.mkv")

    # set the video properties
    video.set_title(f"Video #{uuid.uuid4()}")
    video.set_default_language("en-US")
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status("unlisted")

    # uploading video and printing the results
    video = channel.upload_video(video)
    print(video.id)
    print(video)

