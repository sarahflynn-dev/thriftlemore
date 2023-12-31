# Imports
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re
from datetime import datetime
from flask_app.models import items, reviews

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
        query = "SELECT * FROM users WHERE email = %(email)s;"
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

    # VALIDATE USER
    @staticmethod
    def validate_user(data):
        is_valid = True

        # FIRST NAME VALIDATION
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters long.", "register")
            is_valid = False

        # LAST NAME VALIDATION
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters long.", "register")
            is_valid = False

        # DATE OF BIRTH VALIDATION
        if data['date_of_birth'] == "":
            flash("Date of birth must be entered.", "register")
            is_valid = False

        # FUTURE DATE OF BIRTH VALIDATION
        if data['date_of_birth'] > str(datetime.now()):
            flash("Date of birth must be in the past.", "register")
            is_valid = False

        # USERNAME VALIDATION

        if len(data['username']) < 2:
            flash("Username must be at least 2 characters long.", "register")
            is_valid = False

        # EMAIL VALIDATION
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address.", "register")
            is_valid = False

        # PASSWORD VALIDATION
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False

        if len(data['confirm_password']) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False

        # CONFIRM PASSWORD VALIDATION
        if data['password'] != data['confirm_password']:
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
