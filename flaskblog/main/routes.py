from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route(
    '/')  # Ako zelimo imati vise od jedne route na istu stranicu..tako ce primjerice / i /home otvoriti home.html
@main.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)  # za pagination dio
    return render_template("home.html",
                           posts=posts)  # Ovaj posts = post sluzi za hvatanja tih varijabli unutar htmla. Sad unutar htmla moemo pristupiti tim var


@main.route('/about')
def about():
    return render_template("about.html", title="Naslov")
