from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectFieldBase, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from app.models import User
from wtforms.fields.html5 import DecimalRangeField



class Dockerfiles(FlaskForm):
    name = StringField('Image:Tag', validators=DataRequired)
    dockerfile = FileField("Dockerfile", validators= FileRequired('Choose a File'))



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField(
#         'Repeat Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different username.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user is not None:
#             raise ValidationError('Please use a different email address.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField('New password', validators=[
        InputRequired(),
        EqualTo('new_password2', 'Passwords must match.')
    ])
    new_password2 = PasswordField('Confirm new password',
                                  validators=[InputRequired()])
    submit = SubmitField('Update password')

class TextForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Submit")

# class CreateImages_Dockerfile_Text(FlaskForm):
#     image_tag = TextForm("Image:Tag", validators=[DataRequired()])
#     Dockerfile = TextAreaField("Dockerfile", validators=[DataRequired()])

# class CreateImages_Dockerfile(FlaskForm):
#     image_tag = TextForm("Image:Tag", validators=[DataRequired()])
#     Dockerfile = FileField("Dockerfile", validators=[DataRequired()])

class Container_Run(FlaskForm):
    image = StringField("image:tag",validators=[DataRequired()])
    name = StringField("name_container", validators=[DataRequired()])
    auto_remove = BooleanField("Auto Remove")
    # command and logging
    command = StringField("command")
    entryPoint = StringField("Entry Point")
    dir_working = StringField("Dir Working")
    user = StringField("User")
    # console = RadioField("Console")
    console = BooleanField('Label')
    # always_pull = BooleanField("Always Pull Images")
    # -- Volumes --
    containers = StringField("Containers")
    bind_volumes = RadioField('Label', choices = [('bind', 'description'), ('volumes', 'whatever')])
    rw = RadioField('Label', choices=[('Writeable', 'description'), ('Read-only', 'whatever')])
    # --NETWORK--
    network = SelectField("netwrok" , choices=[('cpp', 'bridge'), ('py', 'host'), ('text', 'none')])
    hostname = StringField("Hostname")
    domain_name = StringField("Domain")
    mac_address = StringField("Mac Address")
    ipv4 = StringField("IPv4")
    ipv6 = StringField("IPv6")
    prim_dns = StringField("Primary DNS")
    sec_dns = StringField("Secondary DNS")
    host_external = StringField("Host External")

    # --Environment--
    name_env = StringField("Name")
    val_env = StringField("Value")

    # --Labels--
    name_label = StringField("Name")
    val_label = StringField("Value")

    # --RestartPolicy--
    restart = RadioField("Restart Policy", choices=[('never', 'never'), ('always', 'always'), ('onfailure', 'onfailure'), ('unless-stopped', 'unless-stopped')])

    # --resource--
    mem_reservation = DecimalRangeField('Memory Reservation', default=0)
    memory = DecimalRangeField('Memory Limit', default=0)
    cpu = DecimalRangeField('CPU limit', default=0)
    submit = SubmitField('Run')


class DockerfileForm(FlaskForm):
    name = StringField("e.g. image:tags", validators=[DataRequired])
    # dockerfile_text = TextAreaField("docker text", validators=[DataRequired])
    dockerfile = FileField("file of Dockerfile", validators=[DataRequired])
    submit = SubmitField('Build')




