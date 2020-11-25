from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []
idx = 1
counter = 1

@app.route('/')
def show_homepage():
    """shows the user the title of the survey, the instructions, and a button to start the survey."""
    return  render_template('index.html', survey=satisfaction_survey)

@app.route('/questions/<int:idx>')
def handle_questions(idx):
    """When the user arrives at one of these pages, it should show a form asking the current question, and listing the choices as radio buttons."""
    global counter

    # questions/1 doesn't have an answer, so don't inlclude "None" in responses
    if idx > 1:
        answer = request.args.get('answer', None)
        responses.append(answer)

    # If user attempts to change url: user is unable to go backwards, user is unable to go forwards by 2 or more. But user can go forward 1.
    # What needs to be different so that if user increments url by 1, they will be redirected back to counter.
    path = request.path
    if request.path == f"/questions/{counter}":
        if idx - 1 < len(satisfaction_survey.questions):
            idx += 1
            counter += 1
            return render_template('questions.html', survey=satisfaction_survey, idx=idx, path=path, counter=counter)
        else:
            return render_template('thank-you.html', responses=responses)
    else:
        counter -= 1
        return redirect(f'/questions/{counter}')          
 
