# Imports
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_bcrypt import Bcrypt
import re

# Email Format Validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Creating a User Class
class User:

    db = "thriftelmore_schema"

    # Constructor
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.date_of_birth = data['date_of_birth']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.items = []

    # SAVE USER
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, date_of_birth, username, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(date_of_birth)s, %(username)s, %(password)s, NOW(), NOW());
        """

        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    # GET ALL USERS
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL(cls.db).query_db(query)

        users = []

        for row in results:
            users.append(cls(row))

        return users

    # GET USER BY EMAIL
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])

    # GET USER BY ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        return cls(results[0])
    
    # was missing login! at least, i didnt find it
    # VALIDATE LOGIN
    @staticmethod
    def validate_login(form_data):    
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email or password.","login")
            return False

        user = User.get_by_email(form_data)
        if not user:
            flash("Invalid email or password.","login")
            return False
        
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email or password.","login")
            return False
        
        return user

    # VALIDATE USER
    @staticmethod
    def validate_user(user):
        is_valid = True

        # FIRST NAME VALIDATION
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters long.", "register")
            is_valid = False

        # LAST NAME VALIDATION
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters long.", "register")
            is_valid = False

        # EMAIL VALIDATION
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "register")
            is_valid = False

        # DATE OF BIRTH VALIDATION
        if user['date_of_birth'] == "":
            flash("Date of birth must be entered.", "register")
            is_valid = False

        # FUTURE DATE OF BIRTH VALIDATION
        if user['date_of_birth'] > str(request.form['today']):
            flash("Date of birth cannot be in the future.", "register")
            is_valid = False

        # USERNAME VALIDATION
        if len(user['username']) < 2:
            flash("Username must be at least 2 characters long.", "register")
            is_valid = False

        # PASSWORD VALIDATION
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False

        # CONFIRM PASSWORD VALIDATION
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.", "register")
            is_valid = False

        return is_valid

    # UNIQUE EMAIL VALIDATION
    @staticmethod
    def validate_unique_email(user):
        is_valid = True

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)

        if len(results) >= 1:
            flash("Email already in use.", "register")
            is_valid = False

        return is_valid

    # UNIQUE USERNAME VALIDATION
    @staticmethod
    def validate_unique_username(user):
        is_valid = True

        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(User.db).query_db(query, user)

        if len(results) >= 1:
            flash("Username already in use.", "register")
            is_valid = False

        return is_valid