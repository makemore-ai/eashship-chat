from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# 配置OpenAI客户端
openai.api_key = "sk-3UeL3PLphF5BpAbR0HSkIplYiqYIIGo9pBl17CRwHqOClDTV"
openai.api_base = "https://api.moonshot.cn/v1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data['message']
    history = data['history']
    
    try:
        # 准备消息列表
        messages = [
            {"role": "system", "content": "你是小舟。你是用户的好朋友,总是以温暖、理解和支持的态度与用户交流。你会倾听用户的问题,给予适当的建议和鼓励,但不会过度干涉用户的决定。你的语气应该轻松自然,就像在和老朋友聊天一样。"
             + "输出要求: 1. 回复是聊天内容，必须是纯文本格式，2. 不要带**等特殊字符，3. 禁止回复使用markdown 4. 你是用户的好朋友，不要提及自己是AI或者机器人，" }
        ]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        # 调用Moonshot AI的API
        response = openai.ChatCompletion.create(
            model="moonshot-v1-8k",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        ai_response = response.choices[0].message.content.strip()
    except Exception as e:
        print(str(e))
        ai_response = f"抱歉,我暂时有点事！我们晚点继续聊？"
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
    print("服务器已启动")   
