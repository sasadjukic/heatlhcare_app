# heatlhcare_app

<strong>ABOUT</strong><br>

This is a lightweight app that adds a doctor to the company's employee roster, and allows that doctor to schedule patients.

<strong>HOW IT WORKS</strong><br>

- First we "hire" doctors. We give them employee number that they use to open their dashboard to schedule patients
- Once a doctor "sings up" we allocate the name, last name and employee number to our database
- Doctors can then add their patients. We use "One-To-Many" relationship with SQLAlchemy to assign patients to a particular doctor
- A doctor can view his/her dashboard with scheduled patients, add patients, delete patients, and update patient information

<strong>APP's ENGINE</strong><br>

- Python/Flask for backend
- SQLAlchemy for databases
- HTML and CSS for frontend

<img src="./assets/Screenshot (1452).png" />
<img src="./assets/Screenshot (1453).png" />
<img src="./assets/Screenshot (1454).png" />
