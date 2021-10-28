#!/usr/bin/python

import logging
import twitch
import urllib.request
import os
import google_api
import re


if __name__ == "__main__":
    VIDEO_PATH = "clips"
    if not os.access(VIDEO_PATH, os.F_OK):
        os.mkdir(VIDEO_PATH)


if __name__ == "__main__":
    twitch.get_bearer_token()


REGEX_TWITCH_MP4 = re.compile(r'^(http.*)-preview-[0-9]+x[0-9]+.jpg$')


def main():
    games_id = map(lambda x: x["id"], twitch.get_top_games(
        first=100)["json"]["data"])

    for streamer in twitch.get_live_streamer(games_id, first=100)["json"]["data"]:
        clips = twitch.get_clips(streamer["user_id"], first=5)[
            "json"]["data"]

        best_clip = max(clips, key=(lambda x: x["view_count"]))

        bc_video_url = None
        bc_video_id, bc_id, bc_title, bc_thumbnail_url, bc_broadcaster_name = best_clip[
            "video_id"], best_clip["id"], best_clip["title"], best_clip["thumbnail_url"], best_clip['broadcaster_name']

        if twitch_regex := REGEX_TWITCH_MP4.search(bc_thumbnail_url):
            bc_video_url = twitch_regex.group(1) + ".mp4"
        else:
            continue

        # check if file exists
        # out_path = os.path.join(VIDEO_PATH, f"{bc_id}.mp4")
        # if os.access(out_path, os.F_OK):
        #     continue

        try:
            urllib.request.urlretrieve(bc_video_url,
                                       os.path.join(VIDEO_PATH, f"{bc_id}.mp4"))
        except Exception as e:
            print(e)
            continue

        try:
            google_api.upload_yt(bc_video_id, bc_id, bc_title,
                                 bc_thumbnail_url, bc_broadcaster_name)
        except Exception as e:
            print(e)
            continue

        print(f"{bc_id}.mp4 is uploaded to youtube")


if __name__ == '__main__':
    main()
