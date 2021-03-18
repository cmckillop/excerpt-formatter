from typing import Optional
import os

import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from settings import FRONTEND_DIR
from models import (
    FormatterRequest,
    MessageRequest,
)
from slack_manager import SlackManager
from text_formatter import TextFormatter

DIST_DIR = FRONTEND_DIR.joinpath("dist")
PUBLIC_DIR = FRONTEND_DIR.joinpath("public")

app = FastAPI()

# noinspection PyTypeChecker
app.mount("/dist", StaticFiles(directory=DIST_DIR), name="dist")

slack_manager = SlackManager()
text_formatter = TextFormatter()


@app.get("/")
async def read_root():
    # noinspection PyTypeChecker
    return FileResponse(
        PUBLIC_DIR.joinpath("index.html"), media_type="text/html"
    )


@app.post("/format")
async def format_text(formatter_request: FormatterRequest):
    if formatter_request.offset_time:
        text_formatter.feed_delay = formatter_request.offset_time
        formatted_input = text_formatter.get_lines(
            text=formatter_request.text,
            preserve_paragraphs=formatter_request.preserve_paragraphs,
        )
    else:
        formatted_input = text_formatter.get_lines(
            text=formatter_request.text,
            preserve_paragraphs=formatter_request.preserve_paragraphs,
            no_offset=True,
        )
    if formatted_input.excerpt_number == 0:
        excerpt_number = formatter_request.segment_count
    else:
        excerpt_number = formatted_input.excerpt_number
    return {
        "excerpt_number": excerpt_number,
        "formatted_text": formatted_input.text,
        "word_count": formatted_input.word_count,
    }


@app.post("/slack/message")
async def send_message(message_request: MessageRequest):
    if message_request.excerpt_number:
        slack_message = (
            f"*Part {message_request.excerpt_number}*\n"
            f"Words: {message_request.word_count}\n"
            f"```{message_request.text}```"
        )
    else:
        slack_message = (
            f"Words: {message_request.word_count}\n"
            f"```{message_request.text}```"
        )
    (
        slack_manager.post_message(
            auth_token=message_request.slack_api_key,
            channel_id=message_request.channel_id,
            message_text=slack_message,
        )
    )
    return {"ok": True}


@app.get("/slack/authenticate")
async def check_token(auth_token: Optional[str] = Header(None)):
    if auth_token:
        authentication_details = slack_manager.authentication_functional(
            auth_token
        )
        if authentication_details["ok"]:
            return {"ok": True, "team": authentication_details["team"]}
    return {"ok": False}


@app.get("/slack/channel/{channel_id}")
async def check_channel(
    channel_id: str, auth_token: Optional[str] = Header(None)
):
    return slack_manager.get_channel_name(auth_token, channel_id)


def main():
    print(f"Production Env: {os.getenv('IS_PRODUCTION')}")
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
