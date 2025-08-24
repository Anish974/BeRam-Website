from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from beram import mail
from beram import PROJECTS_DATA, NEWS_DATA # Import shared data

main_bp = Blueprint('main', __name__)

# Define scientist data here or load from a file
scientists = [
    {'name': 'C.V. RAMAN', 'img': 'img/scientist_cv_raman.jpg'},
    {'name': 'Homi J. Bhabha', 'img': 'img/scientist_bhabha.jpg'},
    {'name': 'A.P.J. Abdul Kalam', 'img': 'img/scientist_kalam.jpg'},
    {'name': 'Vikram Sarabhai', 'img': 'img/scientist_sarabhai.jpg'},
    {'name': 'Jagadish Chandra Bose', 'img': 'img/scientist_bose.jpg'},
    {'name': 'Srinivasa Ramanujan', 'img': 'img/scientist_ramanujan.jpg'},
    {'name': 'Satyendra Nath Bose', 'img': 'img/scientist_sn_bose.jpg'},
    {'name': 'Salim Ali', 'img': 'img/scientist_salim_ali.jpg'},
    {'name': 'Aryabhata', 'img': 'img/scientist_aryabhata.jpg'},
    {'name': 'M. Visvesvaraya', 'img': 'img/scientist_visvesvaraya.jpg'},
]

# Define stats data
stats = [
    {'icon': 'fas fa-project-diagram', 'value': '6+', 'label': 'Projects in Progress'},
    {'icon': 'fas fa-users', 'value': '9+', 'label': 'Team Members'},
    {'icon': 'fas fa-people-arrows', 'value': '12,000+', 'label': 'People will be Impactful'},
    {'icon': 'fas fa-industry', 'value': '4+', 'label': 'Industrial Innovation'},
]


@main_bp.route('/')
def index():
    # Get first few projects and news items for the homepage
    featured_projects = list(PROJECTS_DATA.values())[:2] # Show first 2 projects
    latest_news = NEWS_DATA[:3] # Show latest 3 news items
    return render_template('index.html',
                           title='BeRAM - Advanced Drone Solutions & Innovation',
                           featured_projects=featured_projects,
                           latest_news=latest_news,
                           scientists=scientists,
                           stats=stats)

@main_bp.route('/about')
def about():
    return render_template('about.html', title='About BeRAM')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    # Form handling with email sending
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        inquiry_type = request.form.get('inquiry_type')
        subject = request.form.get('subject')
        message_text = request.form.get('message')

        # Validate form data
        errors = []
        if not name:
            errors.append('Name is required')
        if not email or '@' not in email:
            errors.append('A valid email is required')
        if not inquiry_type:
            errors.append('Please select an inquiry type')
        if not subject:
            errors.append('Subject is required')
        if not message_text:
            errors.append('Message is required')

        # If there are validation errors, flash them and return to the form
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('contact.html', title='Contact Us')

        # Create email content
        email_subject = f"BeRAM Website Contact: {subject}"
        email_body = f"""New message from the BeRAM website contact form:

Name: {name}
Email: {email}
Inquiry Type: {inquiry_type}
Subject: {subject}

Message:
{message_text}

---
This message was sent from the BeRAM website contact form."""

        try:
            # Create and send email
            msg = Message(
                subject=email_subject,
                recipients=['Contactberam@gmail.com'],  # Company email
                body=email_body,
                sender='Contactberam@gmail.com',  # From address
                reply_to=email  # Reply to the sender's email
            )
            mail.send(msg)

            # Send confirmation email to the user
            confirmation_msg = Message(
                subject="Thank you for contacting BeRAM",
                recipients=[email],
                body=f"""Dear {name},

Thank you for contacting BeRAM - Bhandarkar Excellences of Research and Management. We have received your message regarding '{subject}'.

Our team will review your inquiry and get back to you as soon as possible.

Best regards,
BeRAM Team
Contactberam@gmail.com
https://www.linkedin.com/company/beram-bhandarkar-excellences-of-research-and-management/""",
                sender='Contactberam@gmail.com'
            )
            mail.send(confirmation_msg)

            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            # Log the error in a production environment
            print(f"Error sending email: {e}")
            flash('There was an issue sending your message. Please try again later or contact us directly via email.', 'danger')

        return redirect(url_for('main.contact'))

    return render_template('contact.html', title='Contact Us')

@main_bp.route('/mission-statement')
def mission_statement():
    return render_template('mission_statement.html', title='Our Mission')

@main_bp.route('/internship')
def internship():
    return render_template('internship.html', title='Internship Opportunities')

@main_bp.route('/mentorship')
def mentorship():
    return render_template('mentorship.html', title='Mentorship Program')

# @main_bp.route('/about')
# def about():
#     return render_template('about.html', title='about us')

@main_bp.route('/blog')
def blog():
    return render_template('blog.html', title='Our blogs')

@main_bp.route('/pre-order')
def pre_order():
    return render_template('pre_order.html', title='Pre-Order - BeRAM Drones')

@main_bp.route('/request-demo')
def request_demo():
    return render_template('request_demo.html', title='Request Demo - BeRAM Drones')
