from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# DeepSeek API 配置
API_KEY = os.getenv('DEEPSEEK_API_KEY')
BASE_URL = "https://api.deepseek.com"

@app.route('/generate-content', methods=['GET'])
def generate_content():
    try:
        # 调用 DeepSeek API
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个英文口语老师，帮助用户学习日常英文表达。"},
                {"role": "user", "content": "生成新的日常英文口语表达，并附带中文翻译和使用场景示例。"}
            ],
            "max_tokens": 150
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '未生成有效内容')

        if content:
            # 将生成的内容保存到 daily_content.txt
            with open("daily_content.txt", "w", encoding="utf-8") as file:
                file.write(content)
            return jsonify({"content": content}), 200
        else:
            return jsonify({"error": "生成内容失败"}), 500

    except Exception as e:
        return jsonify({"error": f"发生错误: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

