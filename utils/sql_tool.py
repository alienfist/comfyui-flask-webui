import os
import sqlite3
import hashlib
from datetime import datetime
from config import PROJECT_FOLDER, SQL_NAME
from utils.common import get_md5


class Sqlite3Db(object):
    def __init__(self, db_name=f'{PROJECT_FOLDER}{SQL_NAME}.db'):
        self.db_name = db_name
        self.conn = self.get_conn()
        self.initialize_db()

    def initialize_db(self):
        if not os.path.exists('db_initialized.flag'):
            self.create_users_table()
            self.create_images_table()
            with open('db_initialized.flag', 'w') as f:
                f.write('Database initialized')
            print("Database initialized.")

    def get_conn(self):
        try:
            conn = sqlite3.connect(self.db_name)
            print(f"Connected to database '{self.db_name}' successfully.")
            return conn
        except sqlite3.Error as e:
            print(f"Failed to connect to database '{self.db_name}': {e}")
            return None

    def close_conn(self):
        if self.conn:
            self.conn.close()
            print(f"Connection to database '{self.db_name}' closed.")

    def execute_query(self, query, params=None):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.conn.commit()
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Failed to execute query '{query}': {e}")
            return None

    def create_users_table(self):
        """
        role 1 商户 2 普通用户
        statue 2 正常 7 删除
        """
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid CHAR(32) UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone_number TEXT,
                role INTEGER DEFAULT 1,
                status INTEGER DEFAULT 2,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modify_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        try:
            self.execute_query(create_table_sql)
        except sqlite3.Error as e:
            print(f"Failed to create users table: {e}")
            return None

    def create_images_table(self):
        create_images_table_sql = '''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uuid CHAR(32) UNIQUE,
                image_url TEXT NOT NULL,
                params TEXT,
                image_type INTEGER,
                status INTEGER DEFAULT 2,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modify_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        try:
            self.execute_query(create_images_table_sql)
        except sqlite3.Error as e:
            print(f"Failed to create images table: {e}")
            return None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def insert_user(self, username, password, phone_number, role):
        if self.get_user_by_username(username):
            print(f"User '{username}' already exists.")
            return None

        hashed_password = self.hash_password(password)
        current_time = datetime.now()
        insert_user_sql = '''
            INSERT INTO users (uuid, username, password, phone_number, role, create_time, modify_time) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        try:
            uuid = get_md5(f"username:{username}", 16)
            return self.execute_query(insert_user_sql, (uuid, username, hashed_password, phone_number, role, current_time, current_time))
        except sqlite3.Error as e:
            print(f"Failed to insert user: {e}")
            return None

    def get_user_by_username(self, username):
        get_user_sql = '''
            SELECT * FROM users WHERE username = ?
        '''
        try:
            return self.execute_query(get_user_sql, (username,))
        except sqlite3.Error as e:
            print(f"Failed to get user: {e}")
            return None

    def update_user(self, username, new_password):
        hashed_password = self.hash_password(new_password)
        current_time = datetime.now()
        update_user_sql = '''
            UPDATE users SET password = ?, modify_time = ? WHERE username = ?
        '''
        try:
            return self.execute_query(update_user_sql, (hashed_password, current_time, username))
        except sqlite3.Error as e:
            print(f"Failed to update user: {e}")
            return None

    def del_user(self, username):
        update_user_sql = '''
            UPDATE users SET status = 7 WHERE username = ?
        '''
        try:
            return self.execute_query(update_user_sql, (username,))
        except sqlite3.Error as e:
            print(f"Failed to del user: {e}")
            return None

    def verify_password(self, username, password):
        hashed_password = self.hash_password(password)
        user = self.get_user_by_username(username)
        if user:
            stored_password = user[0][3]
            return stored_password == hashed_password
        return False

    def insert_image(self, image_url, params, image_type):
        current_time = datetime.now()
        insert_image_sql = '''
            INSERT INTO images (uuid, image_url, params, image_type, create_time, modify_time) VALUES (?, ?, ?, ?, ?, ?)
        '''
        try:
            uuid = get_md5(f"image:{image_url}", 20)
            return self.execute_query(insert_image_sql, (uuid, image_url, params, image_type, current_time, current_time))
        except sqlite3.Error as e:
            print(f"Failed to insert image: {e}")
            return None

    def get_image_by_id(self, image_id):
        get_image_sql = '''
            SELECT * FROM images WHERE id = ?
        '''
        try:
            return self.execute_query(get_image_sql, (image_id,))
        except sqlite3.Error as e:
            print(f"Failed to get image by id: {e}")
            return None

    def get_images_by_page(self, limit, offset):
        get_images_sql = '''
            SELECT * FROM images ORDER BY create_time DESC LIMIT ? OFFSET ?
        '''
        try:
            return self.execute_query(get_images_sql, (limit, offset))
        except sqlite3.Error as e:
            print(f"Failed to get images by page: {e}")
            return None

    def update_image(self, image_id, image_url=None, params=None, image_type=None):
        current_time = datetime.now()
        update_fields = []
        update_values = []

        if image_url is not None:
            update_fields.append("image_url = ?")
            update_values.append(image_url)
        if params is not None:
            update_fields.append("params = ?")
            update_values.append(params)
        if image_type is not None:
            update_fields.append("image_type = ?")
            update_values.append(image_type)

        update_fields.append("modify_time = ?")
        update_values.append(current_time)
        update_values.append(image_id)

        update_image_sql = f'''
            UPDATE images SET {', '.join(update_fields)} WHERE id = ?
        '''
        try:
            return self.execute_query(update_image_sql, update_values)
        except sqlite3.Error as e:
            print(f"Failed to update image: {e}")
            return None
