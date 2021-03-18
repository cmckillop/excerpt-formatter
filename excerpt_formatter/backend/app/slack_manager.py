import requests


class SlackManager:
    @staticmethod
    def authentication_functional(auth_token: str):
        response = requests.post(
            url="https://slack.com/api/auth.test",
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        return response

    @staticmethod
    def _post_request(auth_token: str, url: str, payload: dict):
        return requests.post(
            url=url, json=payload,
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    @staticmethod
    def _get_request(auth_token: str, url: str, payload: dict):
        return requests.get(
            url=url, params=payload, headers={"Authorization":
                                              f"Bearer {auth_token}"}
        )

    def post_message(self, auth_token: str, channel_id: str, message_text: str):
        payload = {
            "channel": channel_id,
            "text": message_text,
            "icon_emoji": ":speech_balloon:",
            "username": "Excerpt Bot",
        }
        self._post_request(
            auth_token, "https://slack.com/api/chat.postMessage", payload
        )

    def delete_message(self, auth_token: str, channel_id: str, timestamp: str):
        payload = {"channel": channel_id, "ts": timestamp}
        self._post_request(auth_token, "https://slack.com/api/chat.delete", payload)

    def get_channel_info(self, auth_token: str, channel_id: str):
        return self._get_request(
            auth_token,
            "https://slack.com/api/conversations.info",
            {"channel": channel_id},
        ).json()

    def get_channel_name(self, auth_token: str, channel_id: str):
        channel_info = self.get_channel_info(auth_token, channel_id)
        print(channel_info)
        if "channel" in channel_info:
            if "name" in channel_info["channel"]:
                return {"ok": True, "name": channel_info["channel"]["name"]}
        else:
            return channel_info


def delete_message(auth_token: str, channel_id: str, timestamp: str):
    slack_manager = SlackManager()
    slack_manager.delete_message(
        auth_token=auth_token, channel_id=channel_id, timestamp=timestamp
    )
