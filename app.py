# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# @app.route('/home')
# def home():
#     return 'Hello, World!'
# @app.route('/user/<user_name>/<int:user_id>')
# def user(user_name, user_id):
#     return f'Hello, {user_name}({user_id})!'
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
app = Flask(__name__)
 
@app.route('/userLogin', methods = ['POST'])
def userLogin():
    user = request.get_json()#json 데이터를 받아옴
    return jsonify(user)# 받아온 데이터를 다시 전송
 
@app.route('/environments/<language>')
def environments(language):
    return jsonify({"language":language})
 
 
if __name__ == "__main__":
    app.run()
