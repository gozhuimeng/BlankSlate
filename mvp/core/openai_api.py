import requests
import json


class OpenAIAPI:
    def __init__(self, base_url, model_id):
        self.base_url = (
            base_url if base_url[-1] == "\\" or base_url[-1] == "/" else base_url + "/"
        )
        self.model_id = model_id

    def api_test(self, max_tokens=5):
        messages = [{"role": "user", "content": "test"}]
        response = self.chat(messages, max_tokens, 0)
        try:
            result = response.json()
            content = result["choices"][0]["message"]["reasoning_content"]
            if content is not None and content != "":
                return True
            return False
        except Exception as e:
            return False

    def chat(self, messages, max_tokens=0, temperature=0.3, stream=False, tools=[]):
        data = {
            "model": self.model_id,
            "stream": stream,
            "messages": messages,
            "tools": tools,
            "temperature": temperature,
        }
        if max_tokens > 0:
            data["max_tokens"] = max_tokens
        # print(data)
        chat_url = self.base_url + "chat/completions"
        # print(chat_url)
        if stream:
            response = requests.post(chat_url, json=data, stream=True)
        else:
            response = requests.post(chat_url, json=data)
        # print(response.text)
        return response
        # return json.dumps({"choice": [{"message": {"reasoning_content": "pass"}}]})

    @staticmethod
    def append_content(ctx: list[dict[str, str]], role, content):
        ctx.append({"role": role, "content": content})
        return ctx
