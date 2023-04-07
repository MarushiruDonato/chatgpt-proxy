# -*- coding: utf-8 -*-
# @Time : 2023/4/7 13:15
# @Author : Robert G
# @Email : gsc1997@foxmail.com
# @File : proxy.py
# @Desc :
import json

import requests
from flask import Flask, request, jsonify, Response, stream_with_context

app = Flask("proxy")

target_url = "https://api.openai.com/"
auth_secret = "<a hard to guess secret>"


@app.route("/<path:path>", methods=["POST"])
def proxy(path):
    if path != "v1/chat/completions":
        return jsonify({}), 404
    url = target_url + path
    data = request.json

    required_keys = ["model", "stream"]
    for key in required_keys:
        if key not in data:
            return jsonify({"msg": key + " is required."}), 401

    # auth is required in request body
    if "auth" not in data:
        return jsonify({}), 401
    if data["auth"] != auth_secret:
        return jsonify({}), 401
    del data["auth"]

    headers = {
        "Authorization": request.headers.get("Authorization"),
        "Content-Type": request.headers.get("Content-Type")
    }
    stream = data["stream"]
    resp = requests.post(url=url, headers=headers, json=request.json, stream=stream)

    if stream:
        return Response(stream_with_context(resp.iter_content()), content_type=resp.headers["content-type"])
    stat = resp.status_code
    res = json.loads(resp.text)
    return jsonify(res), stat


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
