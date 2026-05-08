## OpenAI API

### 请求格式

- 请求体

```json
{
  "model": "model_name",
  "stream": "is_stream",
  "message": [
    { "role": "system", "content": "system prompt" },
    { "role": "user", "content": "user prompt" },
    { "role": "assistant", "content": "assistant response" }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "tools_name",
        "description": " desc",
        "parameters": {
          "type": "object",
          "properties": {
            "param1": "int",
            "param2": "str"
          },
          "required": ["param1"]
        }
      }
    }
  ]
}
```

- 响应体

```text
# 响应推理内容
data: {"id":"chatcmpl-wowgd2xcrq8yl3i0tnsdc","object":"chat.completion.chunk","created":1778230065,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"reasoning_content":"用户"},"logprobs":null,"finish_reason":null}]}
data: {"id":"chatcmpl-wowgd2xcrq8yl3i0tnsdc","object":"chat.completion.chunk","created":1778230065,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"reasoning_content":"。"},"logprobs":null,"finish_reason":null}]}
data: {"id":"chatcmpl-wowgd2xcrq8yl3i0tnsdc","object":"chat.completion.chunk","created":1778230065,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"reasoning_content":"\n"},"logprobs":null,"finish_reason":null}]}
# 响应内容
data: {"id":"chatcmpl-wowgd2xcrq8yl3i0tnsdc","object":"chat.completion.chunk","created":1778230065,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"content":"生成的"},"logprobs":null,"finish_reason":null}]}
data: {"id":"chatcmpl-wowgd2xcrq8yl3i0tnsdc","object":"chat.completion.chunk","created":1778230065,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"content":"随机"},"logprobs":null,"finish_reason":null}]}
data: {"id":"chatcmpl-wowgd2xcrq8yl3i0tnsdc","object":"chat.completion.chunk","created":1778230065,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{},"logprobs":null,"finish_reason":"stop"}]}
# 请求使用工具
data: {"id":"chatcmpl-s83q17txv5oo6k71akizl","object":"chat.completion.chunk","created":1778230285,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"tool_calls":[{"index":0,"id":"841199783","type":"function","function":{"name":"get_random_int","arguments":""}}]},"logprobs":null,"finish_reason":null}]}
data: {"id":"chatcmpl-s83q17txv5oo6k71akizl","object":"chat.completion.chunk","created":1778230285,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{"tool_calls":[{"index":0,"type":"function","function":{"arguments":"{}"}}]},"logprobs":null,"finish_reason":null}]}
data: {"id":"chatcmpl-s83q17txv5oo6k71akizl","object":"chat.completion.chunk","created":1778230285,"model":"qwen3.5-9b","system_fingerprint":"qwen3.5-9b","choices":[{"index":0,"delta":{},"logprobs":null,"finish_reason":"tool_calls"}]}
# 响应结束
data: [DONE]
```

#### 部分示例代码

```python
import requests
import json

message = {
    "model": "qwen3.5-9b",
    "stream": True,
    "messages": [
        {"role": "user", "content": "请调用tools生成一个随机数"},
        {
            "role": "assistant",
            "content": "\n\n",
            "tool_calls": [
                {
                    "type": "function",
                    "id": "486724779",
                    "function": {"name": "get_random_int", "arguments": "{}"},
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": "486724779",
            "name": "get_random_int",
            "content": "10",
        },
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_random_int",
                "description": "生成一个随机数",
                "parameters": {"type": "object", "properties": {}},
            },
        }
    ],
}

url = "http://10.0.0.190:1234/v1/chat/completions"

response = requests.post(url, json=message, stream=True)
response.encoding = "utf-8" # -> 此处需要设置编码，否则可能会使用错误的解码方式
# print(response.text)    # -> stream 为 False 时使用的打印，只能在非流式输出使用

for line in response.iter_lines(decode_unicode=True):
    if line:
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            print(chunk)
```

## Sqlite3

- 基础用法

```python
import sqlite3

conn = sqlite3.connect("path/database.db")
conn.row_factory = sqlite3.Row  # -> 设置以字典形式响应而并非元组

cur = conn.cursor()

cur.execute("SQL")

conn.commit()

conn.close()
```

- 读取数据

```python
rows = conn.excute("SQL").fetchall()

for row in rows:
    print(row["name"])
# or
print(row[0]["name"])

```
