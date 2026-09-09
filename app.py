from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "cambia-esto-por-una-clave-secreta-larga"
csrf = CSRFProtect(app)

DB = "database.db"