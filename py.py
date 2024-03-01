# ------------------------------- Импорт библиотек -------------------------------
from flask import Flask, render_template, request, session, redirect,url_for
import psycopg2
import os
from werkzeug.security import generate_password_hash,check_password_hash
# ------------------------------- Настройка Flask и БД -------------------------------
def connectionbd():
    connection = psycopg2.connect(
        user="postgres",
        password="123",
        host="78.141.227.124",
        port="5432",
        database="lapka"
    )
    return connection

# Создание экземпляра приложения Flask и установка секретного ключа для сессии
app = Flask(__name__)
app.secret_key = 'ljknijhbhbivuyuilfi9guohi[iypgohi565496468546865648665246879kjbyf6t76t7fyu8]'
# ------------------------------- Вспомогательные функции -------------------------------
#     Функции для взаимодействия с базой данных и выполнения различных операций

# Функция для получения продуктов из базы данных в зависимости от категории и поискового запроса
def fetch_products(category_id, query=None):
    connection = connectionbd()
    cursor = connection.cursor()
    if query:
        sql_query = "SELECT product_id, name, description, price, stock_quantity, map_p FROM products WHERE product_id IN (SELECT product_id FROM product_categories WHERE category_id = %s) AND name ILIKE %s"
        cursor.execute(sql_query, (category_id, '%' + query + '%'))
    else:
        sql_query = "SELECT product_id, name, description, price, stock_quantity, map_p FROM products WHERE product_id IN (SELECT product_id FROM product_categories WHERE category_id = %s)"
        cursor.execute(sql_query, (category_id,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

# Функция для получения деталей конкретного продукта
def fetch_product_details(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    cursor.execute("SELECT product_id,name, description, price, stock_quantity, map_p FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()
    return product

# Функция для добавления товара в корзину пользователя в базе данных
def add_to_cart_db(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cart_id = 1  # Пример, замените на актуальный идентификатор корзины пользователя
        cursor.execute("INSERT INTO cart (cart_id, product_id) VALUES (%s, %s)", (cart_id, product_id))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при добавлении товара в корзину: {e}")
    finally:
        cursor.close()
        connection.close()

# Функция для удаления товара из корзины пользователя в базе данных
def remove_from_cart_db(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при удалении товара из корзины: {e}")
    finally:
        cursor.close()
        connection.close()

# Функция для получения данных о товарах в корзине пользователя из базы данных
def get_cart_data_from_db(cart_items):
    connection = connectionbd()
    cursor = connection.cursor()
    cart_data = []
    for product_id in cart_items:
        cursor.execute("SELECT name, price, map_p FROM products WHERE product_id = %s", (product_id,))
        product_data = cursor.fetchone()
        if product_data:
            cart_data.append({
                'product_id': product_id,
                'name': product_data[0],
                'price': product_data[1],
                'image_url': product_data[2].replace('./static/', '/static/')
            })
    cursor.close()
    connection.close()
    return cart_data

# Функция для получения количества определенного товара в корзине пользователя
def get_product_quantity_from_cart(product_id):
    connection = connectionbd()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT quantity FROM cart WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Ошибка при получении количества товара из корзины: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

# Функция для обновления количества товара в корзине пользователя
def update_cart_quantity(product_id, new_quantity):
    connection = connectionbd()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE cart SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при обновлении количества товара в корзине: {e}")
    finally:
        cursor.close()
        connection.close()
    pass

# Функция для получения отзывов пользователей из базы данных
def get_reviews_from_db():
    connection = connectionbd()
    cursor = connection.cursor()
    cursor.execute("SELECT cust_name, feedback_text, feedback_date FROM feedback")
    reviews = cursor.fetchall()
    cursor.close()
    connection.close()
    return [{'cust_name': row[0], 'feedback_text': row[1], 'feedback_date': row[2]} for row in reviews]

# Функция для сохранения отзыва пользователя в базе данных
def save_feedback_to_db(name, feedback):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        # Предположим, что у вас есть поле customer_name в таблице feedback
        cursor.execute("INSERT INTO feedback (cust_name, feedback_text) VALUES (%s, %s)", (name, feedback))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при добавлении отзыва в базу данных: {e}")
    finally:
        cursor.close()
        connection.close()
# ------------------------------- Маршруты Flask Animals-------------------------------
#            Определение маршрутов для обработки HTTP-запросов в приложении
@app.route('/')
def mainp():
    connection = connectionbd()
    cursor = connection.cursor()
    cursor.execute('SELECT name, map, links FROM categories')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('html.html', postgres_data=data)

@app.route('/cats')
def cats():
    query = request.args.get('query')
    data = fetch_products(2, query)
    return render_template('catc.html', postgres_data=data)

@app.route('/dogs')
def dogs():
    query = request.args.get('query')
    data = fetch_products(1, query)
    return render_template('catd.html', postgres_data=data)

@app.route('/rodents')
def rodents():
    query = request.args.get('query')
    data = fetch_products(3, query)
    return render_template('catr.html', postgres_data=data)

@app.route('/birds')
def birds():
    query = request.args.get('query')
    data = fetch_products(4, query)
    return render_template('catb.html', postgres_data=data)

# ------------------------------- Маршруты Flask Products -------------------------------

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = fetch_product_details(product_id)
    if product:
        print(product[5],flush=True)
        return render_template('prods.html',
                               product_id=product[0],
                               product_name=product[1],
                               product_description=product[2],
                               product_price=product[3],
                               product_stock=product[4],
                               product_image_url=product[5])
    else:
        return "Продукт не найден", 404

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = []

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        if product_id:
            product_id = int(product_id)
        action = request.form.get('action')

        if action == 'add' and product_id not in session['cart']:
            session['cart'].append(product_id)
            add_to_cart_db(product_id)
        elif action == 'remove' and product_id in session['cart']:
            session['cart'].remove(product_id)
            remove_from_cart_db(product_id)

        session.modified = True

    cart_data = get_cart_data_from_db(session['cart'])
    total = sum(float(item['price']) for item in cart_data)
    return render_template('cart.html', cart_data=cart_data, total=total)
#     cart_data = get_cart_data_from_db(session['cart'])
#     total = sum(float(item['price']) * get_product_quantity_from_cart(item['product_id']) for item in cart_data)
#     return render_template('cart.html', cart_data=cart_data, total=total)
@app.route('/add_to_cart', methods=['POST'])

def add_to_cart():
    product_id = request.form.get('product_id')
    if product_id:
        product_id = int(product_id)
        if 'cart' not in session:
            session['cart'] = []
        if product_id not in session['cart']:
            session['cart'].append(product_id)
            add_to_cart_db(product_id)  # Используйте вспомогательную функцию для добавления товара в БД
        session.modified = True
    return redirect(request.referrer or '/')

def add_to_cart_db(product_id):
    connection = connectionbd()
    cursor = connection.cursor()
    try:
        cart_id = 1  # Пример, замените на актуальный идентификатор корзины пользователя
        cursor.execute("INSERT INTO cart (cart_id, product_id) VALUES (%s, %s)", (cart_id, product_id))
        connection.commit()
    except Exception as e:
        print(f"Ошибка при добавлении товара в корзину: {e}")
    finally:
        cursor.close()
        connection.close()


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if product_id in session.get('cart', []):
        session['cart'].remove(product_id)
        remove_from_cart_db(product_id)  # вызов функции удаления из БД
        session.modified = True

    return redirect(url_for('cart'))


@app.route('/feedback')
def feedback():
    reviews = get_reviews_from_db()
    return render_template('feedback.html', feedbacks=reviews)



@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']  # Получение имени пользователя из формы
    feedback = request.form['feedback']  # Получение текста отзыва из формы

    save_feedback_to_db(name, feedback)  # Сохранение отзыва в базе данных

    return redirect('/feedback')  # Перенаправление пользователя на страницу с отзывами


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Проверка сессии
    if 'username' in session:
        return redirect("/")  # Перенаправление на главную страницу

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = connectionbd()
        cursor = connection.cursor()

        hashed_password = password  # Здесь должна быть логика хеширования пароля

        try:
            cursor.execute("SELECT * FROM reg WHERE username = %s AND hashed_password = %s", (username, hashed_password))
            user = cursor.fetchall()
            if user:
                # Установка сессии
                session['username'] = username
                return redirect("/")  # Перенаправление на главную страницу

            return "Неверное имя пользователя или пароль", 401
        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return "Ошибка при входе", 500
        finally:
            cursor.close()
            connection.close()

    return render_template('/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']
        city = request.form['city']
        username = request.form['username']
        address = request.form['address']

        if password != confirm_password:
            return "Пароли не совпадают", 400

        #hashed_password = generate_password_hash(password)

        connection = connectionbd()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO reg (first_name, email, phone_number, city, username, hashed_password, address) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (first_name, email, phone_number, city, username, password, address))
            connection.commit()
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return "Ошибка при регистрации", 500
        finally:
            cursor.close()
            connection.close()

        return redirect('/login')

    return render_template('registration.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # Удаление 'username' из сессии
    return redirect("/")  # Перенаправление на страницу входа


@app.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    current_quantity = get_product_quantity_from_cart(product_id)
    action = request.form.get('change')

    if action == 'increase':
        new_quantity = current_quantity + 1
    elif action == 'decrease' and current_quantity > 1:
        new_quantity = current_quantity - 1
    else:
        new_quantity = current_quantity

    update_cart_quantity(product_id, new_quantity)
    return redirect(url_for('cart'))
# Функция для получения количества товара из корзины
def get_product_quantity_from_cart(product_id):
    connection = connectionbd()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT quantity FROM cart WHERE product_id = %s", (product_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Ошибка при получении количества товара из корзины: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

# Функция для обновления количества товара в корзине



@app.route('/pay')
def pay():
    return render_template('pay.html')

app.route('/process_payment')
def process_payment():
    # Получение данных из формы...
    address = request.form.get('address')
    card_name = request.form.get('card_name')
    card_number = request.form.get('card_number')
    card_expiry = request.form.get('card_expiry')
    card_cvv = request.form.get('card_cvv')
    # Предположим, что amount_paid и order_id вы получаете каким-то образом
    amount_paid = 100  # Пример
    order_id = 1       # Пример

    connection = connectionbd()
    cursor = connection.cursor()
    try:
        # Вставка данных карты в таблицу card_details
        cursor.execute("INSERT INTO card_details (card_number, card_expiry_date, card_cvv, card_holder_name) VALUES (%s, %s, %s, %s) RETURNING card_id", 
                       (card_number, card_expiry, card_cvv, card_name))
        card_id = cursor.fetchone()[0]

        # Вставка записи транзакции в таблицу transactions
        cursor.execute("INSERT INTO transactions (order_id, payment_method, amount_paid, card_id) VALUES (%s, %s, %s, %s)", 
                       (order_id, 'Credit Card', amount_paid, card_id))

        connection.commit()
    except Exception as e:
        print(f"Ошибка при обработке платежа: {e}")
        connection.rollback()  # Откат в случае ошибкиа
        # Дополнительная обработка ошибок
    finally:
        cursor.close()
        connection.close()

    return redirect("/")

# ------------------------------- Запуск приложения -------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=8000)