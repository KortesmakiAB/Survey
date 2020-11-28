from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
# could also write line #3 this way...
# from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_homepage():
    """shows the user the title of the survey, the instructions, and a start button"""

    return  render_template('index.html', survey=satisfaction_survey)


@app.route('/', methods=['POST'])
def show_homepage_redirect():
    """set session[“responses”] to an empty list AND redirect to the start of the survey"""

    session['responses'] = []

    return redirect('/questions/0')


@app.route('/questions/<int:idx>')
def handle_questions(idx):
    """When the user arrives at one of these pages, it should show a form asking the current question, and listing the choices as radio buttons."""

    # from solution code
    responses = session.get('responses')

    # from solution code
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    # from solution code
    if len(responses) != idx:
        # Trying to access questions out of order.
        flash(f"Invalid question id: {idx}.")
        return redirect(f"/questions/{len(responses)}")

    if idx < len(satisfaction_survey.questions):
        
        return render_template('questions.html', survey=satisfaction_survey, idx=len(responses))


# from solution code
@app.route('/answer', methods=['POST'])
def handle_response():
    """Save response and redirect to next question."""
    responses = session.get('responses')

    answer = request.form.get('answer') 

    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # All of the questions have been answered
        return redirect('/thank-you')
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/thank-you")
def thank_you():
    """Survey complete. Show Thank You page."""

    return render_template("thank-you.html", responses=session['responses'])