from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
import requests

from . import main
from .. import db
from ..models import User, Blog, Comment
from .forms import NewBlogForm, CommentForm
from ..email import mail_message

@main.route("/")
def index():
    all_blogs = Blog.query.order_by(db.desc(Blog.created_at)).limit(15).all()
    try:
        quote = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()['quote']
    except Exception:
        quote = ""
  
    return render_template("index.html", blogs = all_blogs, quote = quote)

@main.route("/blog/new", methods = ['GET', 'POST'])
@login_required
def new_blog():
    form = NewBlogForm()
    if form.validate_on_submit():
        email_list = []
        new_blog = Blog(title = form.title.data, content = form.content.data, user = current_user)
        new_blog_id = new_blog.save()

        all_users = User.query.all()
        for user in all_users:
            email_list.append(user.email)

        mail_message("New blog notification","email/welcome_user",user.email, user=user)
        return redirect(url_for('main.blog_content', blog_id = new_blog_id))

    return render_template("new_blog.html", form = form)

@main.route("/blog/view/<blog_id>", methods = ['GET', 'POST'])
@login_required
def blog_content(blog_id):
    curr_blog = Blog.query.filter_by(id = blog_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(content = form.comment.data, user = current_user, blog = curr_blog)
        new_comment.save()
        return redirect(url_for('main.blog_content', blog_id = blog_id))

    comments = Comment.query.filter_by(blog = curr_blog).all()

    return render_template('blog.html', blog = curr_blog, form = form, comments = comments)

@main.route("/blogs")
def view_blogs():
    all_blogs = Blog.query.order_by(db.desc(Blog.created_at)).all()
    
    return render_template("blogs.html", blogs = all_blogs)

@main.route("/account")
@login_required
def profile():
    user_blogs = Blog.query.filter_by(user = current_user).all()
    return render_template('profile.html', user = current_user, blogs = user_blogs)

@main.route("/blog/delete/<blog_id>")
@login_required
def delete_blog(blog_id):
    to_delete = Blog.query.filter_by(user = current_user, id = blog_id).first()
    if to_delete:
        db.session.delete(to_delete)
        db.session.commit()
        flash("Blog deleted successfully")
        return render_template('delete_response.html')
    else:
        flash("Blog deletion failed")
        return render_template('delete_response.html')
    
@main.route("/blog/update/<blog_id>", methods = ['GET','POST'])
@login_required
def update_blog(blog_id):
    form = NewBlogForm()
    user_change_blog = Blog.query.filter_by(user = current_user, id = blog_id).first()

    if user_change_blog is None:
        return redirect(url_for('main.blog_content', blog_id = blog_id))

    if form.validate_on_submit():
        user_change_blog.title = form.title.data
        user_change_blog.content = form.content.data
        db.session.commit()

        return redirect(url_for('main.blog_content', blog_id = blog_id))

    form.content.data = user_change_blog.content
    return render_template('update.html', form = form, blog = user_change_blog)
    
@main.route("/comment/delete/<comment_id>", methods = ['GET','POST'])
@login_required
def delete_comment(comment_id):
    blog_owner = Comment.query.filter_by(id = comment_id).first().blog.user
    to_delete = Comment.query.filter_by(id = comment_id).first()

    if to_delete.blog.user == blog_owner:
        db.session.delete(to_delete)
        db.session.commit()
        flash("Comment deleted successfully")
        return redirect(url_for('main.review_blog', blog_id = to_delete.blog_id))
    else:
        flash("Comment deletion failed")
        return redirect(url_for('main.profile'))

@main.route("/blog/review/<blog_id>", methods = ['GET', 'POST'])
@login_required
def review_blog(blog_id):
    curr_blog = Blog.query.filter_by(user = current_user).first()
    user_blog_comments = Comment.query.filter_by(blog_id = blog_id).all()

    return render_template('review_blog.html', comments = user_blog_comments)