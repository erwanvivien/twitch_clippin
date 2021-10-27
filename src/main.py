import twitch


twitch.get_bearer_token()
twitch.get_users(["squeezie", "ninja"])

# print(twitch.get_clips('squeezie'))

games_id = map(lambda x: x["id"], twitch.get_top_games(
    first=100)["json"]["data"])


for streamer in twitch.get_live_streamer(games_id, first=100)["json"]["data"]:
    clips = twitch.get_clips(streamer["user_id"], first=100)["json"]["data"]

    best_clip = max(clips, key=(lambda x: x["view_count"]))
    print(best_clip)

    print()
