from werkzeug.security import check_password_hash, generate_password_hash
from pyodbc import Cursor
from app import conn
from flask_login import UserMixin
class Post():

    def  __init__(self, title, author, body, image, id = 0):
        self.id = id
        self.title = title
        self.author = author
        self.body = body
        self.image = image



    def add_post(self):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO [dbo].[Posts](title, author, body, image) VALUES(?, ?, ?, ?)",
         (self.title, self.author, self.body, self.image))

        conn.commit()
        cursor.close()


    def get_posts():
        cursor = conn.cursor()
        sql = "select * from [dbo].[Posts]"

        cursor.execute(sql)
        posts = cursor.fetchall()
        cursor.close()

        return posts
    

    def get_post(id):
        cursor = conn.cursor()
        sql = "select * from [dbo].[Posts] WHERE id=?"

        cursor.execute(sql, [id])
        post = cursor.fetchone()
        cursor.close()

        return post      

    def edit_post(self):
        cursor = conn.cursor()
        cursor.execute("UPDATE [dbo].[Posts] SET title=?, author=?, body=?, image=? WHERE id = ?",
         (self.title, self.author, self.body, self.image, self.id))

        conn.commit()
        cursor.close()


class User(UserMixin):
    is_active = True
    def __init__(self, email, password, id = 0):
        self.id = id
        self.email = email
        self.password = password
        self.password_hash = None
        


    def add_user(self):
        cursor = conn.cursor()

        cursor.execute("INSERT INTO [dbo].[Users](email, password_hash) VALUES(?, ?)",
         (self.email, self.generate_pass_hash()))

        conn.commit()
        cursor.close()


    def get_user(email):
        cursor = conn.cursor()
        sql = "select * from [dbo].[Users] WHERE email=?"

        cursor.execute(sql, [email])
        user = cursor.fetchone()
        cursor.close()

        return user

    def get_user_by_id(id):
        cursor = conn.cursor()
        sql = "select * from [dbo].[Users] WHERE id=?"

        cursor.execute(sql, [id])
        user = cursor.fetchone()
        cursor.close()

        new_user = User(id=user[0], email=user[1], password=user[2])
        return new_user

    def generate_pass_hash(self):
        return generate_password_hash(self.password)

    def check_pass_hash(password_hash, password):
        return check_password_hash(password_hash, password)
