from flask import Flask, render_template, request, redirect, url_for
import os
# from flask_dotenv import DotEnv

import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)

app = Flask(__name__)
users = {}
users['anu'] = 'anu'
users['sai'] = 'sai'
users['srinu'] = 'srinu'
users['ali'] = 'ali'

logged_in_user = 0
quantity = 1


@app.route('/')
def signin():
    return render_template('sign_in.html')


@app.route('/shop_catalog')
def shop_catalog():
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM products""")
    # Fetch one record and return result
    products = cursor.fetchall()
    print(products)
    return render_template('shop_catalog.html', products=products)


@app.route('/product_details')
def product_details():
    return render_template('product_details.html')


@app.route('/cart')
def cart():
    cursor = connection.cursor()
    #  usercart = cursor.fetchall()
    #  cursor.execute("""SELECT * FROM usercart WHERE logged_in_user=users[0][0]""")
    # Fetch one record and return result
    usercart = cursor.fetchall()
    return render_template('cart.html')

 
@app.route("/forward/<productid>", methods=['POST'])
def move_forward(productid):

    global logged_in_user

    cur = connection.cursor()
    cur.execute(
        "SELECT * FROM usercart WHERE user_id={} and item_id={}".format(logged_in_user, productid))
    products_in_cart = cur.fetchall()
    if(len(products_in_cart) > 0):
        cur.execute("update usercart set quantity = quantity + 1 where user_id = {} and item_id = {}".format(logged_in_user, productid))
        connection.commit()
    else:
        cur.execute("INSERT INTO usercart(user_id, item_id,quantity) VALUES (?, ?, ?)",
                    (logged_in_user, productid, 1)
                    )
        connection.commit()

    cur.execute("""SELECT * FROM usercart""")
    # Fetch one record and return result
    print("hello")
    usercart = cur.fetchall()
    a = []
    tot_price = 0
    for i in usercart:
        products = []
        product_id = i[2]
        quantity = i[3]
        print(product_id)
        cur.execute("select * from products where id = '{}'".format(product_id))
        products.append(cur.fetchall()[0])
        print(products)
        
        for j in range(0,len(products)):
            price = products[j][3]
            total = int(price) * int(quantity)
            tot_price += total
            arr = [products[j][0],products[j][1],products[j][2],products[j][3],products[j][4],quantity]
            print(arr)
            a.append(arr)
        # print(cur.fetchall())
    # print(products)

    return render_template('cart.html', products=a, total_price = tot_price)



@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            # Create variables for easy access
            Email = request.form['email']
            password = request.form['password']
            cursor = connection.cursor()
            cursor.execute(
                """SELECT * FROM users WHERE email = '{}' AND password = '{}'""".format(Email, password))
            # Fetch one record and return result
            users = cursor.fetchall()
            if users[0][2] == Email and users[0][3] == password:
                global logged_in_user
                logged_in_user = users[0][0]
                return render_template('index.html')

            else:
                return render_template('sign_in.html')
    except IndexError as e:
        return render_template('sign_in.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    Error = request.args['error']

    return render_template('sign_in.html', Error=Error)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    global logged_in_user
    print("hello chheckout")
    cur = connection.cursor()
    
    cur.execute("""SELECT * FROM usercart where user_id={}""".format(logged_in_user))
    # Fetch one record and return result

    usercart = cur.fetchall()
    a = []
    tot_price = 0
    for i in usercart:
        products = []
        product_id = i[2]
        quantity = i[3]
        print(product_id)
        cur.execute("select * from products where id = '{}'".format(product_id))
        products.append(cur.fetchall()[0])
        print(products)
        
        for j in range(0,len(products)):
            price = products[j][3]
            total = int(price) * int(quantity)
            tot_price += total
            arr = [products[j][0],products[j][1],products[j][2],products[j][3],products[j][4],quantity]
            print(arr)
            a.append(arr)
        print(a)
    return render_template('checkout.html', products=a, total_price = tot_price)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    full_name = request.form["Fullname"]
    email = request.form["Email"]
    password = request.form['password']
    cur = connection.cursor()
    cur.execute("INSERT INTO users (full_name, email, password) VALUES (?, ?,?)",
                (full_name, email, password)
                )

    connection.commit()
    users[request.form['Email']] = request.form['password']
    return render_template('sign_in.html')


if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(debug=True, port=port)
