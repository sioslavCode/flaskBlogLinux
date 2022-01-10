import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

from flaskblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # ovo je samo za naziv da nebi slucajno imali dve slie istog naziva
    f_name, f_ext = os.path.splitext(
        form_picture.filename)  # obzirom da ova funckija vraca dvije stvari s liejve strane imamo dvije varijable!!
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static\\profile_pics', picture_filename)
    """ovo sluzi za definrajanje patha gde ce se spremat slike. app roth path nam vrati package path pa onda + static/profile_pics folret i na kraju ime slike
    """

    output_size = (
        125,
        125)  # za resize slike da ne sejvamo ogromnu sliku od 123132mb kad smo u css definirali da je max height 250px
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    form_picture = i

    form_picture.save(picture_path)  # Ovo je sejvalo u filesystem ali u db je i dalje stara slika
    return picture_filename  # obzirom da necemo u ocu fuknciju stavljat sejv u db ajmo user barem vratiti filename


def send_reset_email(user):
    token = user.get_reset_token()  # User model ima fonkciju ovu kojoj je defaut tokena na trajanje sekutni 1800
    msg = Message('Password reset request',  # SUBJECT
                  sender='noreplay@demo.com',
                  # SENDER - ovdje moze doci do spam problema ako se pretvaramo da smo nettko s druge adrese
                  recipients=[user.email])  # RECIPIENT
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If yoo did not make this request just ignore the email.

    '''
    # Ovo external na kraju kaže url_for da će link biti korišten za vansjkukomunikaciju pa da ga stavi cijelog a ne samo dio koji se koristi lokalno u programu (kraći)
    mail.send(msg)
