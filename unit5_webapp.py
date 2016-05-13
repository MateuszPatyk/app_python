from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

# Tutaj definiujemy sobie bazę
class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    firstname = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    status = db.Column(db.String)
    university = db.Column(db.String)
    type = db.Column(db.String)
    field_study = db.Column(db.String)
    study_degree = db.Column(db.String)
    degree = db.Column(db.String)
    average = db.Column(db.Integer)
    question1 = db.Column(db.Integer)
    question2 = db.Column(db.Integer)
    question3 = db.Column(db.Integer)
    question4 = db.Column(db.Integer)
    question5 = db.Column(db.Integer)
    question6 = db.Column(db.Integer)
    question7 = db.Column(db.Integer)
    question8 = db.Column(db.Integer)
    question9 = db.Column(db.Integer)
    question10 = db.Column(db.Integer)
    work = db.Column(db.String)
    hours = db.Column(db.Integer)
    income = db.Column(db.Integer)
    uni_help = db.Column(db.String)

# Tutaj ją inicjalizujemy (troche jak konstruktor)
    def __init__(self, firstname, age, status, university, type, field_study, study_degree, degree, average, question1, question2, question3, question4, question5,  question6, question7, question8, question9, question10, work, hours, income, uni_help):
        self.firstname = firstname
        self.age = age
        self.status = status
        self.university = university
        self.type = type
        self.field_study = field_study
        self.study_degree = study_degree
        self.degree = degree
        self.average = average
        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.question4 = question4
        self.question5 = question5
        self.question6 = question6
        self.question7 = question7
        self.question8 = question8
        self.question9 = question9
        self.question10 = question10
        self.work = work
        self.hours = hours
        self.income = income
        self.uni_help = uni_help
db.create_all()

active_page = [None, None, None, None]

@app.route("/")
def welcome():
	active_page[0] = "active"
	return render_template('welcome.html', active_welcome = active_page[0])


@app.route("/form")
def show_form():
	active_page[1] = "active"
	return render_template('form.html', active_form = active_page[1])

@app.route("/raw")
def show_raw():
	active_page[2] = "active"
    # Wczytaj dane z bazy do obiektu fd i przeslij go do szablonu (jako argument)
	fd = db.session.query(Formdata).all()
	return render_template('raw.html', formdata=fd, active_raw = active_page[2])


@app.route("/result")
def show_result():
	active_page[3] = "active"
    # Wczytaj dane z bazy do obiektu fd_list
	fd_list = db.session.query(Formdata).all()

    # Some simple statistics for sample questions
	question1 = []
	question2 = []
	question3 = []

    # Z obiektu fd_list wczytanego z bazy wybieraj po koleji elementy, aby je przetworzyć np. policzyc średnią i przesłac na wykres
	for el in fd_list:
		question1.append(int(el.question1)) #append -> udostepnione przez pythona dodaje element do listy czyli do listy q1 doda nam elementy q1 z bazy
		question2.append(int(el.question2))
		question3.append(int(el.question3))

	if len(question1) > 0:
		mean_question1 = statistics.mean(question1)
	else:
		mean_question1 = 0

	if len(question2) > 0:
		mean_question2 = statistics.mean(question2)
	else:
		mean_question2 = 0

	if len(question3) > 0:
		mean_question3 = statistics.mean(question3)
	else:
		mean_question3 = 0

    # Prepare data for google charts
    # Postać tuple'a - czyli taki słownik: ['Klucz', wartość]
	data = [['question1', mean_question1], ['question2', mean_question2], ['question3', mean_question3]]

	return render_template('result.html', data=data, active_results = active_page[3])


@app.route("/save", methods=['POST'])
def save():
    # Get data from FORM
     # 'name' z forumalarza musi sie zgadzac z name podanym tutaj np. do zmiennej firstname przypisujemy wartość z forumalarza elementu o nazwie: name="firstname
    firstname = request.form['firstname']
    age = request.form['age']
    status = request.form['status']
    university = request.form['university']
    type = request.form['type']
    field_study = request.form['field_study']
    study_degree = request.form['study_degree']
    degree = request.form['degree']
    average = request.form['average']
    question1 = request.form['question1']
    question2 = request.form['question2']
    question3 = request.form['question3']
    question4 = request.form['question4']
    question5 = request.form['question5']
    question6 = request.form['question6']
    question7 = request.form['question7']
    question8 = request.form['question8']
    question9 = request.form['question9']
    question10 = request.form['question10']
    work = request.form['work']
    hours = request.form['hours']
    income = request.form['income']
    uni_help = request.form['uni_help']
    # Save the data - spakuj zmienne w obiekt klasy Formdata i zapisz w bazie
    fd = Formdata(firstname, age, status, university, type, field_study, study_degree, degree, average, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, work, hours, income, uni_help)
    db.session.add(fd)
    db.session.commit()

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()