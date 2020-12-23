from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,TextAreaField,SelectField,DateField,RadioField
from wtforms.validators import DataRequired,Email

class ContactForm(FlaskForm):

    name=StringField("Full name: ",validators=[DataRequired()])
    email=StringField("Email: ",validators=[DataRequired(),Email(60)])
    phone=StringField("Phone: ",validators=[DataRequired()])
    msg=TextAreaField("Message: ",validators=[DataRequired()])
    Submit=SubmitField("Submit ")

class ApplyForm(FlaskForm):
    name=StringField("Full name ",validators=[DataRequired()])
    email=StringField("Email ",validators=[DataRequired(),Email()])
    phone=StringField("Phone ",validators=[DataRequired()])
    dob=DateField("Date of Birth ",validators=[DataRequired()])
    gender=RadioField("Gender ",choices=[('Male','Male'),('Female','Female')],validators=[DataRequired()])
    school=StringField("Your school name ")
    subj=SelectField(u'Subject you want to learn ', choices=[('Physics','Physics'),
    ('Chemistry','Chemistry'),('Mathematics','Mathematics'),('Biology','Biology'),('Economics','Economics'),
    ('Computer Science','Computer Science'),('English','English')],validators=[DataRequired()])
    marks=IntegerField('Your 10th std percentage in the selected subject',validators=[DataRequired()])
    total_marks=IntegerField('Your aggregate percentage in 10th std ',validators=[DataRequired()])
    Submit=SubmitField("Submit ")
