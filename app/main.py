import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import FormatterRequest, MessageRequest
from app.slack_manager import SlackManager
from app.text_formatter import TextFormatter

app = FastAPI()

app.mount('/dist', StaticFiles(directory='app/dist'), name='dist')

slack_manager = SlackManager()
text_formatter = TextFormatter()


@app.get('/')
async def read_root():
    return FileResponse('app/src/templates/main.html', media_type='text/html')


@app.post('/format')
async def format_text(formatter_request: FormatterRequest):
    if formatter_request.date_time:
        text_formatter.start_date_time = formatter_request.date_time
        formatted_input = text_formatter.get_lines(text=formatter_request.text,
                                                   preserve_paragraphs=formatter_request.preserve_paragraphs)
    else:
        formatted_input = text_formatter.get_lines(text=formatter_request.text,
                                                   preserve_paragraphs=formatter_request.preserve_paragraphs,
                                                   no_offset=True)
    return {'excerpt_number': formatted_input.excerpt_number,
            'formatted_text': formatted_input.text,
            'word_count': formatted_input.word_count}


@app.post('/message')
async def send_message(message_request: MessageRequest):
    if message_request.excerpt_number:
        slack_message = f'*Part {message_request.excerpt_number}*\nWords: {message_request.word_count}\n```{message_request.text}```'
    else:
        slack_message = message_request.text
    (slack_manager.post_message(
        api_token=message_request.slack_api_key,
        channel_id=message_request.channel_id,
        message_text=slack_message))
    return {'ok': True}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8080)
