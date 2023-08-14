import os
import time

import torch
import uvicorn
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from fastapi import FastAPI
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydantic import BaseModel

app = FastAPI()

VIDEO_MODEL = "zeroscope_v2_576w"
# VIDEO_MODEL = "text-to-video-ms-1.7b"

OUT_IP = "127.0.0.1"
# OUT_IP = "{Your-server-IP}"

# the image generated path, default in /var/www/html, if you start a httpd service, you can access by {OUT_IP/video.mp4}
GENERATED_IMAGES_PATH = "/var/www/html"

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, "data")
MODEL_PATH = os.path.join(ROOT_PATH, "models")

pipe = DiffusionPipeline.from_pretrained(os.path.join(MODEL_PATH, VIDEO_MODEL), torch_dtype=torch.float16)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)


class LLMPrompt(BaseModel):
    prompt: str = None
    num_inference_steps: int = 40
    height: int = 320
    width: int = 576
    num_frames: int = 24


@app.post("/generate_video")
def generate_video(lp: LLMPrompt):

    try:
        video_frames = pipe(prompt=lp.prompt, num_inference_steps=lp.num_inference_steps, height=lp.height, width=lp.width, num_frames=lp.num_frames).frames
        timestamp = int(time.time())
        video_name_tmp = f"{VIDEO_MODEL}_{str(timestamp)}_tmp.mp4"
        video_path = export_to_video(video_frames, os.path.join(DATA_PATH, video_name_tmp))
        video = VideoFileClip(video_path)

        video_name = f"{VIDEO_MODEL}_{str(timestamp)}.mp4"
        video.write_videofile(os.path.join(GENERATED_IMAGES_PATH, video_name), codec="libx264", audio_codec="aac")
        return {"success": True, "msg": f"http://{OUT_IP}/{video_name}"}
    except Exception as e:
        return {"success": False, "msg": f"generate error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7861, log_level="info")
