from app.email import send_email
from flask import render_template, current_app

def send_contact_email(form):
    subject = form.subject.data
    fullname = form.fullname.data
    email = form.email.data
    message = form.message.data

    send_email(subject,
               sender=email,
               recipients=[current_app.config['ADMINS'][0]],
               text_body=render_template('contact/email/contact.txt', fullname=fullname, email=email, message=message),
               html_body=render_template('contact/email/contact.html', fullname=fullname, email=email, message=message))
    
    print("Email inviata correttamente")
