from flask import render_template,request,redirect,url_for,abort,flash
from ..requests import get_random_quotes
from . import main
from ..models import User,Comment,Blog,Subscriber
from flask_login import login_required, current_user
from .. import db, photos
from .forms import UpdateProfile,BlogForm,CommentForm
from sqlalchemy import desc

@main.route('/')
def index():
    blogs = Blog.query.all()
    user = User.query.filter_by(id=current_user.get_id()).first()
    current_post = Blog.query.order_by(desc(Blog.id)).all()
    
    '''
    view root function that returns render_template
    '''
    quote = get_random_quotes()
    return render_template('index.html', quote= quote,blogs=blogs,user=user,current_post=current_post)
    
@main.route('/blog', methods=['GET', 'POST'])
@login_required
def new_blog():
    blog_form = BlogForm()
    if blog_form.validate_on_submit():
        title = blog_form.blog_title.data
        category = blog_form.category.data
        content = blog_form.content.data
        created_by = blog_form.created_by.data
        user_id = current_user.id
        new_blog = Blog(title=title, category=category, content=content, user_id=user_id, created_by= created_by)
        new_blog.save_blog()
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.index'))

    else:
        all_blogs = Blog.query.order_by(Blog.date_posted).all()

    return render_template('new_blog.html', blogs=all_blogs,blog_form = blog_form)    
    
    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    all_blogs = Blog.get_current_blog(current_user.id).order_by(Blog.date_posted.desc()).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
    
    
@main.route('/blog/<id>', methods=['GET', 'POST'])
@login_required
def blog_details(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blogs = Blog.query.get(id)
    if blogs is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment=form.comment.data,
            blog_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.comment.data = ''
        flash('Your comment has been posted successfully!')
    return render_template('comments.html', blog=blogs, comments=comments, comments_form=form)    
    
    
@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/update.html', form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        return redirect(url_for('main.profile',uname=uname))
@main.route('/comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comments = Comment(name=form.name.data)
        db.session.add(comments)
        db.session.commit()
        flash('Comment added successfully.')
        return redirect(url_for('.index'))
    return render_template('comments.html', commentform=form)
    

@main.route('/comment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    """
        View delete comment function that returns the delete comment page and its data
    """
    comment = Comment.query.filter_by(id=id).first()
    db.session.delete(comment)
    db.session.commit()

    flash('You have successfully deleted the comment', 'success')
    return redirect(url_for('main.profile', uname=current_user.username)) 
    
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    """
    subscribe function that subscribes the user to the post
    """
    email = request.args.get('email')
    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()
    flash('Email submitted successfully', 'success')
    return redirect(url_for('main.index'))    