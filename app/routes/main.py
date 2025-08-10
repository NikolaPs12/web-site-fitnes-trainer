from flask import Flask, render_template, request, redirect, url_for, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/main.html')