from simple_youtube_api.LocalVideo import LocalVideo
import uuid
VIDEO_TITLE = f"Video #{uuid.uuid4()}"
DEFAULT_LANGUAGE = "en-US"
SET_EMBEDDABLE = True
SET_LICENSE = "creativeCommon"
SET_PRIVACY_STATUS = "public"

def upload_video_to_youtube(channel):
    video = LocalVideo(file_path="recordedVideo.mkv")

    # set the video properties
    video.set_title(VIDEO_TITLE)
    video.set_default_language(DEFAULT_LANGUAGE)
    video.set_embeddable(SET_EMBEDDABLE)
    video.set_license(SET_LICENSE)
    video.set_privacy_status(SET_PRIVACY_STATUS)

    # uploading video and printing the results
    video = channel.upload_video(video)
    print(video.id)
    print(video)

