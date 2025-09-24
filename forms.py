from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from wtforms.fields import EmailField
from wtforms.fields import DateTimeLocalField, TimeField, DateField


the_states= [
    "State*",
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming"
]
class RegisterForm(FlaskForm):
    username = StringField(
        'Username*', validators=[DataRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Username*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})

    email = EmailField(
        'Email*', validators=[DataRequired(), Length(min=6, max=40), Email()], render_kw={"placeholder": "Email*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    password = PasswordField(
        'Password*', validators=[DataRequired(), Length(min=6, max=40)], render_kw={"placeholder": "Password*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    confirm = PasswordField(
        'Repeat Password*', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={"placeholder": "Repeat Password*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    submit = SubmitField("Signup", render_kw={
        "class": "flex items-center justify-center flex-none px-3 py-2 md:px-4 md:py-3 border-2 rounded-lg font-medium border-black bg-black text-white dark:bg-white dark:text-black"})



class LoginForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Email()],  render_kw={"placeholder": "Email*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    password = PasswordField('Password', [DataRequired()],  render_kw={"placeholder": "Password*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={
        "class": "flex items-center justify-center flex-none px-3 py-2 md:px-4 md:py-3 border-2 rounded-lg font-medium border-black bg-black text-white dark:bg-white dark:text-black"})

class UpdateStatForm(FlaskForm):
    form_type = StringField(render_kw={"value": "stat", "hidden": "hidden"})
    first_name = StringField(
        'First Name*', validators=[DataRequired(), Length(min=2, max=40)],
        render_kw={"placeholder": "First Name*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    last_name = StringField(
        'Last Name*', validators=[DataRequired(), Length(min=2, max=40)],
        render_kw={"placeholder": "Last Name*",
                   "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})

    address = StringField(
        'Street Address*', validators=[DataRequired(), Length(min=6, max=40)],
        render_kw={"placeholder": "Street Address*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    state = SelectField("", render_kw={"placeholder": "State*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    city = StringField("City*", render_kw={"placeholder": "City*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    zip = StringField('Zipcode*', validators=[Length(min=5, max=100)], render_kw={"placeholder": "Zipcode*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    unit = StringField("unit/suite", render_kw={"placeholder": "Apt/Unit/Suite", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    phone = StringField(
        'Phone Number*', validators=[DataRequired(), Length(min=10, max=12)],
        render_kw={"placeholder": "Phone Number", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    submit = SubmitField('submit', render_kw={
        "class": "flex items-center justify-center flex-none px-3 py-2 md:px-4 md:py-3 border-2 rounded-lg font-medium border-black bg-black text-white dark:bg-white dark:text-black"})

    def __init__(self):
        super(UpdateStatForm, self).__init__()

        self.state.choices = [(state, state) for state in the_states]

class UpdateEmail_ProfileForm(FlaskForm):
    form_type = StringField(render_kw={"value": "email", "hidden": "hidden"})
    new_email = EmailField(
        'New Email*',
        validators=[DataRequired(), Length(min=6, max=40), Email()], render_kw={"placeholder": "New Email*",
                                                                                "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    email_confirm = EmailField(
        ' Confirm New Email*',
        validators=[DataRequired(), Length(min=6, max=40), Email(), EqualTo('password', message='Emails must match')], render_kw={"placeholder": "Confirm New Email*",
                                                                                "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})

    submit = SubmitField('submit', render_kw={"class":"flex items-center justify-center flex-none px-3 py-2 md:px-4 md:py-3 border-2 rounded-lg font-medium border-black bg-black text-white dark:bg-white dark:text-black"})

class UpdatePassword_ProfileForm(FlaskForm):
    form_type = StringField(render_kw={"value": "password", "hidden": "hidden"})
    old_password = PasswordField('Current Password*', [DataRequired()], render_kw={"placeholder": "Current password*","class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    new_password = PasswordField('Your New Password*', [DataRequired()], render_kw={"placeholder": "New password*","class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    confirm = PasswordField(
        'Repeat New Password*', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')],
        render_kw={"placeholder":"Confirm new password*", "class": "flex px-3 py-2 md:px-4 md:py-3 border-2 border-black rounded-lg font-medium placeholder:font-normal dark:border-white dark:text-white dark:bg-[#0b101a]"})
    submit = SubmitField('submit', render_kw={"class":"flex items-center justify-center flex-none px-3 py-2 md:px-4 md:py-3 border-2 rounded-lg font-medium border-black bg-black text-white dark:bg-white dark:text-black"})


