from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

responses = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "hello-world!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def show_start():
    title = survey.title
    instructions = survey.instructions
    return render_template('instructions.html', title = title, instructions = instructions)

@app.route('/begin', methods=['POST'])
def begin_survey():
    session['responses'] = []
    return redirect('/question/0')

@app.route('/question/<int:i>')
def show_question(i):
    if i != len(responses):
        flash("I don't think so. >:(")
        return redirect(f'/question/{len(responses)}')
    if len(responses) == len(survey.questions):
        flash("Dude you finished, stop being an over achiever")
        return redirect('/complete')
    
    question = survey.questions[i].question
    choices = survey.questions[i].choices
    return render_template('question.html', question = question, choices = choices, i = i+1)

@app.route('/answer', methods=['POST'])
def add_answer():
    choice = request.form["answer"]
    responses.append(choice)

    answers = session['responses']
    answers.append(choice)
    session['responses'] = answers

    if len(responses) == len(survey.questions):
        return redirect('/complete')
    else:
        return redirect(f'/question/{len(responses)}')

@app.route('/complete')
def show_finish():
    return render_template('complete.html')