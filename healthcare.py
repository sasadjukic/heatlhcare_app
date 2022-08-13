
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'veryverysecretive'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healtcareemployees.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Doctors(db.Model, UserMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), nullable = False)
    employee_no = db.Column(db.Integer, nullable = False, unique = True)
    patients = db.relationship('Patients', backref='doctors')

class Patients(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(50), nullable = False, unique = True)
    date = db.Column(db.String(50), nullable = False) 
    time = db.Column(db.String(50), nullable = False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable = False)

@login_manager.user_loader
def load_user(user_id):
    return Doctors.query.get(user_id)

def create_employee_number():

    storage = ''
    for num in range(4):
        num = random.randint(1, 9)
        storage += str(num)

    return int(storage)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/confirmation', methods=['POST'])
def confirm_registration():

    if request.method == "POST":
        name = request.form['name']
        l_name = request.form['last_name']
        employee_no = create_employee_number()
        new_doctor = Doctors(name=name,
                             last_name=l_name,
                             employee_no=employee_no)

        try: 
            db.session.add(new_doctor)
            db.session.commit()
            return render_template('confirmation.html', name=name, l_name=l_name, employee_no=employee_no)

        except:
            return 'There was error creating your profile'

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        employee_number = request.form['employee_no']
        doctor = Doctors.query.filter_by(employee_no=employee_number).first()
        if doctor:
            login_user(doctor)
            return redirect(url_for('dashboard'))

        return 'Invalid employee number'

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    if request.method == 'POST':
        patient_name = request.form['p_name']
        patient_l_name = request.form['p_l_name']
        patient_phone = request.form['p_telephone']
        patient_date = request.form['p_date']
        patient_time = request.form['p_time']
        doctor_id = current_user.id
        new_patient = Patients(name = patient_name, 
                               last_name = patient_l_name,
                               phone = patient_phone,
                               date = patient_date,
                               time = patient_time,
                               doctor_id = doctor_id)

        try:
            db.session.add(new_patient)
            db.session.commit()
            return redirect('/dashboard')

        except:
            return 'There was an error adding a patient'

    else:
        patients = Patients.query.filter_by(doctor_id=current_user.id).order_by(Patients.date).all()
        return render_template('dashboard.html', doctor_name=current_user.name,
                                doctor_last_name=current_user.last_name, patients = patients)

@app.route('/delete/<int:id>')
@login_required
def delete_patient(id):
    patient_to_delete = Patients.query.get_or_404(id)

    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    except:
        return 'Error. Could not delete this patient'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_patient(id):
    patient_to_update = Patients.query.get_or_404(id)

    if request.method == 'POST':
        patient_to_update.name = request.form['p_name']
        patient_to_update.last_name = request.form['p_l_name']
        patient_to_update.phone = request.form['p_telephone']
        patient_to_update.date = request.form['p_date']
        patient_to_update.time = request.form['p_time']

        try: 
            db.session.commit()
            return redirect(url_for('dashboard'))

        except: 
            return 'Error updating patient'

    else:
        return render_template('update.html', patient=patient_to_update)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()