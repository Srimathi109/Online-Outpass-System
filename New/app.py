from flask import Flask, render_template, request, redirect, url_for, session, send_file
import re
import random
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'SSN123'

users = {
    "user@ssn.edu.in": "1234"
}

submitted_forms = {}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "shalusri620@gmail.com"        
app.config['MAIL_PASSWORD'] = "huwvpnqowawutxpr"              
app.config['MAIL_DEFAULT_SENDER'] = 'srimathi2410307@ssn.edu.in' 


mail = Mail(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            msg = "Invalid email or password"
    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html', email=session['email'])
    return redirect(url_for('login'))

@app.route('/apply-outpass', methods=['GET', 'POST'])
def apply_outpass():
    if 'email' not in session:
        return redirect(url_for('login'))

    msg = ""
    success = False
    application_number = None

    if request.method == 'POST':
        phone_number = request.form.get('phone_number', '')
        parent_phone_number = request.form.get('parent_phone_number', '')

        phone_pattern = re.compile(r'^\d{10}$')
        if not phone_pattern.match(phone_number):
            msg = "Invalid student phone number. Must be 10 digits."
        elif not phone_pattern.match(parent_phone_number):
            msg = "Invalid parent's phone number. Must be 10 digits."
        else:
            random_digits = random.randint(10000000, 99999999)
            application_number = f"{random_digits}"

            form_data = {
                'application_number': application_number,
                'digital_id': request.form.get('digital_id'),
                'department': request.form.get('department'),
                'room_number': request.form.get('room_number'),
                'hostel_number': request.form.get('hostel_number'),
                'from_date': request.form.get('from_date'),
                'from_time': request.form.get('from_time'),
                'to_date': request.form.get('to_date'),
                'to_time': request.form.get('to_time'),
                'phone_number': request.form.get('phone_number'),
                'parent_phone_number': request.form.get('parent_phone_number'), 
            }

            try:
                message = Message(
                    subject="Outpass Request Submitted - SSN Outpass",
                    recipients=[session['email']],
                    body=f"Dear user,\n\nYour outpass request has been successfully submitted.\nYour application number is: {application_number}\n\nThank you."
                )
                mail.send(message)
                success = True
                msg = f"Form submitted successfully! Your application number is {application_number}. Confirmation email sent."
                
                submitted_forms[session['email']] = form_data

            except Exception as e:
                msg = f"Failed to send confirmation email: {e}"

    return render_template('outpass.html', msg=msg, success=success, application_number=application_number)

@app.route('/check-status', methods=['GET', 'POST'])
def check_status():
    if 'email' not in session:
        return redirect(url_for('login'))

    status = None
    msg = ""
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query == "":
            msg = "Please enter an Outpass Number"
        else:
            if query == "1234567890":
                status = "Approved"
            elif query == "0987654321":
                status = "Pending Approval"
            else:
                msg = "No outpass application found for the entered information."
    return render_template('status.html', status=status, msg=msg)

@app.route('/download-outpass')
def download_outpass():
    if 'email' not in session:
        return redirect(url_for('login'))

    form_data = submitted_forms.get(session['email'], None)

    if not form_data:
        return "No approved outpass found. Please apply first."

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "SSN Outpass")

    p.setFont("Helvetica", 12)
    y = height - 100
    line_height = 35

    for key, value in form_data.items():
        text = f"{key.replace('_', ' ').title()}: {value}"
        p.drawString(50, y, text)
        y -= line_height

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="Approved_Outpass.pdf", mimetype='application/pdf')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

