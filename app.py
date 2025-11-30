from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email', '').strip()

    if not email or '@' not in email:
        return jsonify({'error': 'Некорректный email'}), 400

    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if bot_token and chat_id:
        try:
            message = f"🔔 Новая подписка на ECOSORT!\n📧 Email: {email}"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print("❌ Ошибка Telegram API:", response.json())
        except Exception as e:
            print("❌ Исключение при отправке в Telegram:", e)

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)