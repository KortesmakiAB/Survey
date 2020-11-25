from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []
idx = 1

@app.route('/')
def show_homepage():
    """shows the user the title of the survey, the instructions, and a button to start the survey."""
    return  render_template('index.html', survey=satisfaction_survey)

@app.route('/questions/<int:idx>')
def handle_questions(idx):
    """When the user arrives at one of these pages, it should show a form asking the current question, and listing the choices as radio buttons."""
    
    answer = request.args.get("answer", None)
    responses.append(answer)

    if idx - 1 < len(satisfaction_survey.questions):
        idx += 1
    else:
        return render_template('thank-you.html')
    return render_template('questions.html', survey=satisfaction_survey, idx=idx-1)

