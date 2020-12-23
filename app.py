from flask import Flask,render_template,url_for,redirect,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import ContactForm,ApplyForm
import stripe 

   
app=Flask(__name__)

stripe.api_key = 'sk_test_51I0BPPJ7NR1mciwGs1cjsPklBAus6sNI0ApsFygdCeKozQunJDQW0YHwbvYx7smYPyy5SLJM5FLzCzOHVrmguVjL007kTG599k'
DOMAIN = 'http://localhost:5000'
app.config['SECRET_KEY']='testkey'

DB_URL = 'postgres://dumcgckialjrcn:71b308b2ce0ee4228e98305fd4d8f39b29e027e9754aca7189aa074d400902e5@ec2-34-200-181-5.compute-1.amazonaws.com:5432/d43t7i91ultdof'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db)

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

class Apply(db.Model):
    
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


@app.route('/',methods=['GET','POST'])
def index():
    form=ApplyForm()

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

        return redirect(url_for('payment')) 

    return render_template("index.html",form=form)

@app.route('/payment',methods=['GET','POST'])
def payment():
    return render_template('payment.html')


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

        return redirect(url_for('index'))
    return render_template('contact.html',form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


@app.route('/create-checkout-session',methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'Learning League',
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=DOMAIN + '/thankyou',
            cancel_url=DOMAIN + '/cancel',
        )
        return jsonify({'id': checkout_session.id})

        
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__=="__main__":
    app.run(debug=True)