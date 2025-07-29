from flask import Flask
import os

app = Flask(__name__)

# [취약점!] DB 비밀번호가 코드에 하드코딩되어 있습니다.
db_password = "my-super-secret-password-123"

@app.route('/')
def hello():
    # 이 비밀번호를 사용한다고 가정
    return f"Hello, World! Using password: {db_password}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
