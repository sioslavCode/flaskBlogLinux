from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New post', form=form, legend='New post')


@posts.route(
    "/post/<int:post_id>")  # kada želimo imati dinamički link. što očekuješ da će biti int, str ili nešto drugo?..
def post(post_id):  # i ojvdje dinamički link tj varijablu kao argument
    post = Post.query.get_or_404(post_id)  # dohvati ako postoji a ako ne onda 404 (page doesne exist)

    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # dohvati ako postoji a ako ne onda 404 (page doesne exist)
    if post.author != current_user:
        abort(403)  # ako ovo nije user koji je napisao post napravi 403 error http forbiden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend='Update post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # dohvati ako postoji a ako ne onda 404 (page doesne exist)
    if post.author != current_user:
        abort(403)  # ako ovo nije user koji je napisao post napravi 403 error http forbiden route
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
