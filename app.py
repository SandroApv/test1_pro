from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Modello per le domande
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    answer_a = db.Column(db.String(100), nullable=False)
    answer_b = db.Column(db.String(100), nullable=False)
    answer_c = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # e.g., 'A', 'B', 'C'

# Homepage - scelte tra quiz e terapia di grido primitivo
@app.route('/')
def home():
    return render_template('index.html')

# Rotta per la pagina del quiz
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

# Rotta per la pagina "terapia di grido primitivo"
@app.route('/scream_therapy')
def scream_therapy():
    return render_template('scream_therapy.html')  # assicurati che questo template esista

# Endpoint per ottenere una domanda casuale
@app.route('/api/question', methods=['GET'])
def get_random_question():
    question = Question.query.order_by(db.func.random()).first()
    return jsonify({
        'id': question.id,
        'question_text': question.question_text,
        'options': {
            'A': question.answer_a,
            'B': question.answer_b,
            'C': question.answer_c
        }
    })

# Endpoint per verificare la risposta
@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.json
    question_id = data.get('id')
    selected_answer = data.get('answer')

    question = Question.query.get(question_id)
    if question and question.correct_answer == selected_answer:
        return jsonify({'result': 'correct'})
    else:
        return jsonify({'result': 'incorrect'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creazione delle tabelle
    app.run(debug=True)
