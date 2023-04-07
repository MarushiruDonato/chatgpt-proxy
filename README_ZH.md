一个用来转发OpenAI请求的代理

用来把请求转发到能访问OpenAI API的服务器

# 怎么用
0. 自定义auth secret

改一下`proxy.py`里的`auth_secret`变量, 随便整个字符串就行

1. 装依赖
```bash
pip install -r requirements.txt
```
2. 跑起来

*首先你跑这个程序的服务器要能访问OpenAI的api*

```bash
python proxy.py
```

或者用gunicorn跑

```bash
pip install gunicorn
gunicorn -w 4 -b "0.0.0.0:5000" proxy:app --log-level=debug
```

3. 发请求

```python
import requests

data = {
    # 别漏了这个auth
    "auth": "<your-custom-auth-secret>",
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Introducing Marushiru Donato."}
    ],
    "temperature": 0.6,
    "stream": True
}
headers = {"Authorization": "Bearer <your-openai-token>"}
resp = requests.post("http://<your-server-ip>:5000/v1/chat/completions", headers=headers, json=data)

```
