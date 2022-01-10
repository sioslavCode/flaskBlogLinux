from flaskblog import db
from datetime import datetime
from flaskblog import login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author',
                            lazy=True)  # Ovo kaze da posts ima releciju s Post modelom/classom. Backref je kao veza. Lazy znaci

    def get_reset_token(self, expires_seconds=1800):
        """Metoda za resetiranje lozinke pomocu generiranja tokena"""
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod  # Primjetiti da funkcija nema self u sebi jer ga niti ne koristi
    def verify_reset_token(token):
        """Za verifikaciju tokema"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}, '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)  # Ovdje se refenciramo na user tockka id. Tj kao fereign key cemo koristiti iz classe user, id polje

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted})"
