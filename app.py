from flask import Flask,render_template,url_for,redirect,request,jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import ContactForm,ApplyForm
import stripe
import smtplib
import os
from flask_login import (LoginManager,UserMixin,login_required,login_user,
                        logout_user,current_user)
 
app=Flask(__name__)

login_manager=LoginManager()

stripe.api_key = 'sk_test_51I0BPPJ7NR1mciwGs1cjsPklBAus6sNI0ApsFygdCeKozQunJDQW0YHwbvYx7smYPyy5SLJM5FLzCzOHVrmguVjL007kTG599k'
DOMAIN = 'https://learning-league-flask.herokuapp.com'
app.config['SECRET_KEY']='testkey'

DB_URL = os.getenv('DB_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db)

login_manager.init_app(app)
login_manager.login_view='index'


class StudentContact(db.Model):
    
    __tablename__='contact_student'
    
    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    email=db.Column(db.Text)
    phone=db.Column(db.Text,unique=True) 
    msg=db.Column(db.Text)

    def __init__(self,name,email,phone,msg):
        self.name=name
        self.email=email
        self.phone=phone
        self.msg=msg

@login_manager.user_loader
def load_user(user_id):
    return Apply.query.get(user_id)

class Apply(db.Model,UserMixin):
    
    __tablename__='applied_users'
    
    user_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    email=db.Column(db.Text)
    phone=db.Column(db.Text)
    dob=db.Column(db.Date)
    gender=db.Column(db.Text)
    school=db.Column(db.Text)
    subj=db.Column(db.Text)
    marks=db.Column(db.Text)
    total_marks=db.Column(db.Text) 

    def __init__(self,name,email,phone,dob,gender,school,subj,marks,total_marks):
        self.name=name
        self.email=email
        self.phone=phone
        self.dob=dob
        self.gender=gender
        self.school=school
        self.subj=subj
        self.marks=marks
        self.total_marks=total_marks
    
    def get_id(self):
        return self.user_id


@app.route('/',methods=['GET','POST'])
def index():
    form=ApplyForm()

    if current_user.is_authenticated:
        logout_user()


    if form.validate_on_submit():
        
        name=form.name.data
        email=form.email.data
        phone=form.phone.data
        dob=form.dob.data
        gender=form.gender.data
        school=form.school.data
        subj=form.subj.data
        marks=form.marks.data
        total_marks=form.total_marks.data

        user=Apply(name,email,phone,dob,gender,school,subj,marks,total_marks)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        import re
        def MagicString(str):
            return re.findall(r'\S+', str)
        temp=MagicString(name)
        name=temp[0]

        next=request.args.get('next')

        if next==None or not next[0]=='/':
            next=f'/payment:{name},{email}'
        

        return redirect(next)

    return render_template("index.html",form=form)




@app.route('/payment:<string:name>,<string:email>',methods=['GET','POST'])
@login_required
def payment(name,email):
    return render_template('payment.html',name=name,email=email)


@app.route('/contact',methods=['GET','POST'])
def contact():
    form=ContactForm()

    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        phone=form.phone.data
        msg=form.msg.data

        student_contact=StudentContact(name,email,phone,msg)

        db.session.add(student_contact)
        db.session.commit()

        flash(f"Thank you {name}, \n \t\t Your message is successfully received. Your feedback is valuable to us.")

        
    return render_template('contact.html',form=form)

@app.route('/thankyou:<string:name>,<string:email>')
@login_required
def thankyou(name,email):
    try:
        user_email=email

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        

        msg = MIMEMultipart()
        msg['From'] = 'dev.mainak.chatterjee@gmail.com'
        msg['To'] = user_email
        msg['Subject'] = 'Learning League Confirmation'

        body = f"""Hello {name},\n \t \t 
        Thank you for your trust. You are successfully enrolled in Learning League. 
        We will send you further details shortly."""
        msg.attach(MIMEText(body,'plain'))

        text = msg.as_string()
    
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('dev.mainak.chatterjee@gmail.com',os.getenv('PASSWORD_DEV_EMAIL'))
        server.sendmail('dev.mainak.chatterjee@gmail.com',user_email,text)
        server.quit()

        logout_user()

        return render_template('thankyou.html',name=name,email=user_email)
    
    except Exception as e:
        redirect(url_for('cancel'))

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


@app.route('/create-checkout-session:<string:name>,<string:email>',methods=['POST'])
@login_required
def create_checkout_session(name,email):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': 10000,
                        'product_data': {
                            'name': 'Learning League',
                            'images': ['https://source.unsplash.com/240x360/?code,coding'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + f'/thankyou:{name},{email}',
            cancel_url=DOMAIN + '/cancel',
        )
        return jsonify({'id': checkout_session.id})

        
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__=="__main__":
    app.run(debug=False)
    
    