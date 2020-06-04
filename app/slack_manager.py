import requests


class SlackManager:

    @staticmethod
    def post_message(api_token, channel_id: str, message_text: str):
        payload = {
            'channel': channel_id,
            'text': message_text,
            'icon_emoji': ':speech_balloon:',
            'username': 'Excerpt Bot'
        }

        requests.post(
            url='https://slack.com/api/chat.postMessage',
            json=payload,
            headers={'Authorization': f'Bearer {api_token}'}
        )
