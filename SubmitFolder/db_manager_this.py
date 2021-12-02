"""DB transactions module"""
import sqlite3


class appDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # perm ADMIN(manager)-2, Employee-1, customer-0
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Customers(
        id_customer   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        email         TEXT    NOT NULL,
        password      TEXT    NOT NULL,
        full_name     TEXT    NOT NULL,
        phone         INT     NOT NULL,
        perm          INT     NOT NULL DEFAULT (0)
        )""")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Products(
        id_product    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        product_name  TEXT    NOT NULL,
        product_price DOUBLE  NOT NULL,
        stock      INTEGER NOT NULL
        )""")

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Orders(
        id_order       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_customer    INTEGER NOT NULL,
        id_product     INTEGER NOT NULL,
        quantity       INTEGER NOT NULL,
        order_date     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (id_customer) REFERENCES Customers (id_customer) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        FOREIGN KEY (id_product) REFERENCES Products (id_product) 
        ON DELETE SET NULL
        ON UPDATE CASCADE
        )""")

        if self.is_customer_exists("admin") == 1:
            self.create_admin_user("admin", "admin123", "admins_user", 111111111, 2)

        self.conn.commit()

    def add_user_db(self, email, password, full_name, phone):
        self.cur.execute("""
        INSERT INTO Customers
        (email, password, full_name, phone)
        VALUES (?, ?, ?, ?)
        """, (email, password, full_name, phone)
        )
        self.conn.commit()

    def create_admin_user(self, email, password, full_name, phone, perm):
        self.cur.execute("""
        INSERT INTO Customers
        (email, password, full_name, phone, perm)
        VALUES (?, ?, ?, ?, ?)
        """, (email, password, full_name, phone, perm)
        )
        self.conn.commit()

    def is_customer_exists(self, email):
        # 0 = user email exist in our db
        # 1 = user email does not exist our db
        self.cur.execute("SELECT exists(SELECT 1 FROM Customers WHERE email=?)", (email,))
        if self.cur.fetchone()[0] == 1:
            return 0
        else:
            return 1

    def get_all_customers(self):
        self.cur.execute("SELECT * FROM Customers")
        rows = self.cur.fetchall()
        return rows

    def get_customer_id(self, email):
        # if login success returns user id and user perm
        self.cur.execute("""
        SELECT id_customer
        FROM Customers
        WHERE email=?
        """, (email)
        )
        found = self.cur.fetchone()
        if found is None:
            return None
        else:
            return found[0],found[1]
        
    def get_customer_name(self, email):
        # if login success returns user id and user perm
        self.cur.execute("""
        SELECT id_customer
        FROM Customers
        WHERE email=?
        """, (email)
        )
        found = self.cur.fetchone()
        if found is None:
            return None
        else:
            return found[0],found[1]

    def get_customer_info(self, id_customer):
        # if login success returns user id and user perm
        self.cur.execute("""
        SELECT id_customer, email, password, full_name, phone, perm
        FROM Customers
        WHERE id_customer=?
        """, (id_customer,)
        )
        return self.cur.fetchall()

    
    def get_user_perm(self, email, password):
        # if login success returns user id and user perm
        self.cur.execute("""
        SELECT id_customer, perm
        FROM Customers
        WHERE email=? and password=?
        """, (email, password)
        )
        found = self.cur.fetchone()
        if found is None:
            return False, -1
        else:
            return found[0], found[1]
        
    def get_user_password(self, email):
        # if login success returns user id and user perm
        self.cur.execute("""
        SELECT password
        FROM Customers
        WHERE email=?
        """, (email,)
        )
        found = self.cur.fetchone()
        if found is None:
            return False#, -1
        else:
            return found[0]#, found[1]
        
    def get_all_products(self):
        self.cur.execute("""
        SELECT id_product, product_name, product_price, stock 
        FROM Products
        """)
        return self.cur.fetchall()

    def is_product_exists(self, product_name):
        self.cur.execute(
        "SELECT exists(SELECT 1 FROM Products WHERE product_name=?)", (product_name,)
        )
        if self.cur.fetchone()[0] > 0:
            return True
        else: return False

    def add_product(self, name, price, stock):
        self.cur.execute("""
        INSERT INTO Products
        (product_name, product_price, stock)
        VALUES (?,?,?)
        """, (name, price, stock))
        self.conn.commit()

    def get_product(self, id_product):
        self.cur.execute(
        """
        SELECT id_product, product_name, product_price, stock
        FROM Products
        WHERE id_product=?
        """,
        (id_product,))
        return self.cur.fetchone()

    def delete_product(self, id_product):
        self.cur.execute("DELETE FROM Products WHERE id_product=?", (id_product,))
        self.conn.commit()

    def update_product(self, id_product, name, price, stock):
        self.cur.execute("""
        UPDATE Products
        SET product_name=?, product_price=?, stock=?
        WHERE id_product=?
        """, (name, price, stock, id_product)
        )
        self.conn.commit()

    def update_customer(self, id_customer, password, full_name, email, phone):
        self.cur.execute("""
        UPDATE Customers
        SET password=?, full_name=?, email=?, phone=?
        WHERE id_customer=?
        """, (password, full_name, email, phone, id_customer,)# price, stock, id_product)
        )
        self.conn.commit()

    def get_all_product(self):
        self.cur.execute("""
        SELECT * FROM Products
        """)
        
    def add_order(self, id_customer, id_product, quantity):
        self.cur.execute("""
        INSERT INTO Orders
        (id_customer, id_product, quantity)
        VALUES (?, ?, ?)
        """,(id_customer, id_product, quantity))
        self.conn.commit()
        
    def get_customer_order(self, id_customer):
        self.cur.execute("""
        SELECT * FROM Orders WHERE id_customer=?
        """, (id_customer,))
        self.cur.fetchall()
        
    def get_this_order(self, id_customer, id_product):
        self.cur.execute("""
        SELECT * FROM Orders WHERE id_customer=? AND id_product=?
        """, (id_customer,id_product))
        self.cur.fetchall()
        
    def get_all_orders(self):
        self.cur.execute("""
        SELECT * FROM Orders
        """)
        return self.cur.fetchall()

    def get_product_price(self, id_product):
        self.cur.execute("""
        SELECT product_price FROM Products WHERE id_product=?
        """, (id_product,))
        return self.cur.fetchone()

    def get_product_name(self, id_product):
        self.cur.execute("""
        SELECT product_name FROM Products WHERE id_product=?
        """, (id_product,))
        return self.cur.fetchone()

    def get_all_orders_customer(self, customer_id):
        self.cur.execute("""
        SELECT * FROM Orders WHERE id_customer=?
        """, (customer_id,))
        return self.cur.fetchall()
    
    def remove_order(self, order_id):
        self.cur.execute("DELETE FROM Orders WHERE id_order=?", (order_id,))
        self.conn.commit()