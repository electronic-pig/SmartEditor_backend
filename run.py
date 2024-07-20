from app import create_app

app = create_app()


# 为了方便测试，添加一个简单的路由
@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
