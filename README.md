# Text2Video
Text2Video Multi-model Experience Center


## Supported LLMs

| Video LLMs            | Supported   | Model Type | Notes |
|-----------------------|-------------|------------|-------|
| zeroscope_v2_576w     | Yes         | Local      |       |
| text-to-video-ms-1.7b | Yes         | Local      |       |
| Gen-2                 | Coming soon | Proxy      |       |

## Installation

- Download video models from huggingface, and install the relevant dependencies.

```commandline
git lfs install
git clone https://huggingface.co/damo-vilab/text-to-video-ms-1.7b

# git lfs install
# git clone https://huggingface.co/cerspense/zeroscope_v2_576w

pip install -r requirements.txt


# to make package `moviepy` works, install FFmpeg firstly, otherwise you can't open video dirrectly.
sudo yum install epel-release
sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
sudo yum install ffmpeg
ffmpeg -version
```

- start project.

```commandline

# Start in Local environment.
python main.py

# Start in Pord environment, you should modify param `OUT_IP` in main_prod.py.
nohup python main_prod.py > text2video.log &

```

## Configuration

- you can change the model in main.py, `zeroscope_v2_576w` is default.

```python

VIDEO_MODEL = "zeroscope_v2_576w"
# VIDEO_MODEL = "text-to-video-ms-1.7b"
```

## Usage

```commandline
curl -X POST -H "Content-Type: application/json" -d '{
"prompt": "A beautiful girl walks through the mall with a cup of milk tea, her hair blowing in the wind",
"height": 200,
"width": 576,
"num_frames": 24
}' http://120.27.193.115:7861/generate_video
```

```json
{
    "success": true,
    "msg": "http://120.27.193.115:7861/girl.mp4"
}
```

https://github.com/xuyuan23/Text2Video/assets/26043513/56e5bf3b-409e-4f52-a059-57d899b1b0a3

