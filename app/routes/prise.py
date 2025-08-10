from flask import Blueprint, render_template

prise_bp = Blueprint('prise', __name__)

@prise_bp.route('/prise')
def prise():
    return render_template('prises/prise.html')