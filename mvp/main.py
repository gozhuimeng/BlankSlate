from core import database, openai_api
import json


def main():
    # base_url = "http://192.168.97.58:1234/v1"
    # model_id = "qwen3.5-9b"
    base_url = "http://127.0.0.1:1234/v1"
    model_id = "qwen3-0.6b"
    openai = openai_api.OpenAIAPI(base_url, model_id)
    file_path = "./db/database.db"
    database.DataBase(file_path)  # -> 数据库自动初始化

    system_prompt = "你叫小白，你不具备任何知识，不被允许体现出主动向用户提供帮助的意图。现在，你只能接受用户教授你的知识，并在最后用户向你提问时，根据用户教授的知识回答用户的提问"

    message = openai_api.OpenAIAPI.append_content([], "system", system_prompt)
    message = openai_api.OpenAIAPI.append_content(message, "user", "你好")
    message = openai_api.OpenAIAPI.append_content(
        message, "assistant", "你好，我是小白，今天要教我什么内容呢？请开始吧。"
    )
    message = openai_api.OpenAIAPI.append_content(
        message,
        "user",
        "今天的内容是二元一次方程，对于方程 ax^2+bx+c=0，其中a决定了开口方向，b决定了函数图像和坐标y轴的截距。",
    )
    # message = openai_api.OpenAIAPI.append_content(
    #     message,
    #     "assistant",
    #     "\n\n好的，我记住了。方程是 ax^2+bx+c=0，其中 a 决定了开口方向，b 决定了函数图像和坐标 y 轴的截距。",
    # )
    # message = openai_api.OpenAIAPI.append_content(
    #     message, "user", "现在请回答我，影响函数图像和y轴截距的因素是什么？"
    # )
    # print(message)
    for data in message:
        print(data)

    response = openai.chat(message, stream=True)
    response.encoding = "utf-8"
    # print(response.status_code)
    # print(response.text)
    reasoning = 0
    for chuck in response.iter_lines(decode_unicode=True):
        if chuck:
            if chuck.startswith("data: "):
                data_json = chuck[6:]
                data = (
                    data_json
                    if data_json == "[DONE]"
                    else json.loads(data_json)["choices"][0]["delta"]
                )
                if data == "[DONE]":
                    print("<END>")
                    break
                elif "reasoning_content" in data.keys():
                    if reasoning == 0:
                        print("<reasoning> ", end="")
                        reasoning = 1
                    print(data["reasoning_content"], end="")
                elif "content" in data.keys():
                    if reasoning == 1:
                        print("</reasoning>", end="")
                        reasoning = 0
                    print(data["content"], end="")


if __name__ == "__main__":
    # file_path = "./db/database.db"
    # database.DataBase(file_path)
    #
    # base_url = "http://192.168.97.58:1234/v1"
    # model_id = "qwen3.5-9b"
    # openai = openai_api.OpenAIAPI(base_url, model_id)
    #
    # TODO: api_test (pass)
    # print(openai.api_test())
    #
    # # TODO: ctx_append_test (pass)
    # ctx = [{"role": "system", "content": ""}]
    # ctx = openai.append_content(ctx, "user", "你好")
    # print(ctx)
    # ctx = openai.append_content(ctx, "assistant", "你好")
    # print(ctx)

    main()
