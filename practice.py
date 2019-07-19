# 2019-07-13
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

orders = [] # global variable을 하나 만들기. 전체 함수에서 쓰일 변수
order_no = 1

## HTML을 주는 부분
@app.route('/')
def home():
    return 'This is Home!'

## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def post():
    global orders # 주문 받기
    global order_no

    name_receive = request.form['name_give']  # 클라이언트로부터 이름을 받는 부분
    number_receive = request.form['number_give']  # 클라이언트로부터 개수를 받는 부분
    address_receive = request.form['address_give']  # 클라이언트로부터 주소를 받는 부분
    phone_receive = request.form['phone_give']  # 클라이언트로부터 폰번호를 받는 부분

    order = {'name':name_receive,'number':number_receive, 'address': address_receive, 'phone number': phone_receive, 'no': order_no} # 받은 걸 딕셔너리로 만들고,
    orders.append(order)   # 넣는다
    order_no += 1
    return jsonify({'result':'success'})

@app.route('/delete', methods=['POST'])
def delete():
    global orders              # 이 함수 안에서 나오는 orders 글로벌 변수를 가리킵니다.
    no_receive = request.form['no_give']

    for order in orders:
        if str(order['no']) == no_receive:
            orders.remove(order)
            return jsonify({'result': 'success'})
    return jsonify({'result': 'fail', 'msg': '삭제할 주문이 없습니다.'})

@app.route('/order', methods=['GET'])
def view():
    if not orders:
        return jsonify({'result': 'fail', 'msg': '주문이 없습니다.'})
    return jsonify({'result':'success', 'orders':orders})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)