import requests
import os

# DeepSeek API 配置
API_KEY = os.environ.get('DEEPSEEK_API_KEY')
BASE_URL = "https://api.deepseek.com"

def fetch_daily_content():
    try:
        url = f"{BASE_URL}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个英文口语老师，帮助用户学习日常英文表达。"},
                {"role": "user", "content": "生成十条关于餐厅点餐的日常英文口语表达，并附带中文翻译和使用场景示例。"}
            ],
            "max_tokens": 150
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        
        if content:
            with open("daily_content.txt", "w", encoding="utf-8") as file:
                file.write(content)
            print("内容生成成功！")
        else:
            print("API 未返回有效内容。")

    except Exception as e:
        print(f"发生错误: {e}")
        raise  # 抛出异常以便 GitHub Actions 识别失败

if __name__ == "__main__":
    fetch_daily_content()
