a proxy for forwarding OpenAI chat completion requests

# Usage

1. install requirements

```bash
pip install -r requirements.txt
```

2. run the server

*Note: Your server has to be in the region which has access to OpenAI APIs.*

```bash
python proxy.py
```

or run with gunicon

```bash
pip install gunicorn
gunicorn -w 4 -b "0.0.0.0:5000" proxy:app --log-level=debug
```

4. send requests

```python
import requests

data = {
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

