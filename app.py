from flask import Flask,render_template,request,redirect,g
from flask_login import login_required, current_user, login_user, logout_user
import flask_login
from models import Appointment, UserModel,db,login
 
app = Flask(__name__)
app.secret_key = 'xyz'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 

db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()
     
@app.route('/home')
@login_required
def blog():
    return render_template('home.html')
 
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/home')
     
    return render_template('login.html')
 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/home')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')
 
@app.route('/painting', methods=['POST', 'GET'])
@login_required
def painting():
    if request.method == "POST":
        date = request.form['date']
        time = request.form['time']
        persons = request.form['select']
        c_id = flask_login.current_user.id
        appointment = Appointment(date=date, time=time, rooms_persons=persons, c_id=c_id, service='Painting')
        print(c_id)
        db.session.add(appointment)
        db.session.commit()
        return redirect('/home')
    return render_template('painting.html')


@app.route('/salon', methods=["POST", 'GET'])
@login_required
def salon():
    if request.method == "POST":
        date = request.form['date']
        time = request.form['time']
        persons = request.form['select']
        c_id = flask_login.current_user.id
        appointment = Appointment(date=date, time=time, rooms_persons=persons, c_id=c_id, service='Salon')
        print(c_id)
        db.session.add(appointment)
        db.session.commit()
        return redirect('/home')
    return render_template('salon.html')
 
@app.route('/pnc', methods=["POST", 'GET'])
@login_required
def pnc():
    if request.method == "POST":
        date = request.form['date']
        time = request.form['time']
        persons = request.form['select']
        c_id = flask_login.current_user.id
        appointment = Appointment(date=date, time=time, rooms_persons=persons, c_id=c_id, service='Plumber/Carpenter')
        print(appointment.time)
        db.session.add(appointment)
        db.session.commit()
        return redirect('/home')
    return render_template('pnc.html')

@app.route('/electrician', methods=["POST", 'GET'])
@login_required
def electrician():
    if request.method == "POST":
        date = request.form['date']
        time = request.form['time']
        c_id = flask_login.current_user.id
        appointment = Appointment(date=date, time=time, c_id=c_id, service='Electrician')
        print(appointment.time)
        db.session.add(appointment)
        db.session.commit()
        return redirect('/home')
    return render_template('electrician.html')

@app.route('/appointments')
@login_required
def bookings():
    booking = Appointment.query.filter_by(c_id=flask_login.current_user.id).all()
    return render_template('appointment.html', booking=booking)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=True)