# Twitch clippin

Twitch Clippin retrieves the most popular clip of the day for the 100 streamers currently live

- 📺 Provides a channel that regroups various clips from twitch
- 🔍 It is easy to find top clips from your favorite streamer
- [<img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/8a805e39049f04d22efe1eed8139d61c5e9a24cc/images/svg/youtube.svg" 
        width=20 
        style="transform: translateY(5px);"/> Youtube Channel
        ](https://www.youtube.com/channel/UCEZdxTHKiRrIbnCEfajOSCg)
- ⚡ We clippin boys

## How to use

```bash
python3 src/main.py
```

## Configuration

Two files are required, you can find more info here
- [Twitch config](/twitch.example.json). This file uses information found on the [Twitch Console](https://dev.twitch.tv/console)
- [Google config](/client_secrets.example.json). This file can be downloaded on your project page on the [Google Console](https://console.cloud.google.com/apis/credentials)

## Packages

Everything is in `requirements.txt`, you should use following command to install dependencies

```bash
pip3 install -r requirements.txt
```
