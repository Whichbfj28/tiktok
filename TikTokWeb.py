#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@Description:TikTok.py
@Date       :2023/01/27 19:36:18
@Author     :imgyh
@version    :1.0
@Github     :https://github.com/imgyh
@Mail       :admin@imgyh.com
-------------------------------------------------
Change Log  :
-------------------------------------------------
'''

from flask import *
from TikTok import TikTok
import argparse

def work(share_link):
    tk = TikTok()

    url = tk.getShareLink(share_link)
    key_type, key = tk.getKey(url)
    if key_type == "aweme":
        datanew, dataraw = tk.getAwemeInfo(key)
    elif key_type == "live":
        datanew = tk.getLiveInfo(key, option=False)
    return datanew


app = Flask(__name__)
# 设置编码
app.config['JSON_AS_ASCII'] = False

def argument():
    parser = argparse.ArgumentParser(description='抖音去水印工具 使用帮助')
    parser.add_argument("--port", "-p", help="Web端口",
                        type=int, required=False, default=5000)
    args = parser.parse_args()

    return args

@app.route("/douyin", methods=["POST"])
def douyin():
    usefuldict = {}
    if request.method == "POST":
        result = request.form
    else:
        usefuldict["status_code"] = 500
        return jsonify(usefuldict)

    try:
        usefuldict = work(result["share_link"])
        usefuldict["status_code"] = 200
    except Exception as error:
        usefuldict["status_code"] = 500
    return jsonify(usefuldict)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    args = argument()
    app.run(debug=False, host="0.0.0.0", port=args.port)
