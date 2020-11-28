from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_homepage():
    """shows the user the title of the survey, the instructions, and a button to 
    fire off a POST request that will set session[“responses”] to an empty list AND start the survey."""
    return  render_template('index.html', survey=satisfaction_survey)

@app.route('/', methods=['POST'])
def show_homepage():
    """set session[“responses”] to an empty list AND redirect to the start of the survey"""
    session['responses'] = []
    return  redirect('/questions/0')

@app.route('/questions/<int:idx>')
def handle_questions(idx):
    """When the user arrives at one of these pages, it should show a form asking the current question, and listing the choices as radio buttons."""

    answer = request.args.get('answer', None)
    responses.append(answer)
    if None in responses:
        responses.pop() 

    # from solution code
    if len(responses) != idx:
        # Trying to access questions out of order.
        flash(f"Invalid question id: {idx}.")
        return redirect(f"/questions/{len(responses)}")

    if idx < len(satisfaction_survey.questions):
        idx += 1
        return render_template('questions.html', survey=satisfaction_survey, idx=idx, responses=responses)
    else:
        return redirect('/thank-you')

@app.route("/thank-you")
def thank_you():
    """Survey complete. Show Thank You page."""

    return render_template("thank-you.html", responses=responses)