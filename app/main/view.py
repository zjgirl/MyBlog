from . import main
from flask_login import login_required, current_user
from flask import render_template, redirect, flash, url_for,request,make_response, abort
from ..model import User, Post, Permission
from ..auth.form import LoginForm
from .form import ProfileForm, PostForm
from ..db import db

@main.route('/', methods = ['GET', 'POST'])
@main.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.body.data, author = current_user._get_current_object())      
        db.session.add(post)
        db.session.commit()      
        return redirect(url_for('.index'))
    show_follow_posts = bool(request.cookies.get('show_follow_posts', ''))
    if show_follow_posts:
        query = current_user.follow_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page,error_out=False)
    posts = pagination.items
    return render_template('index.html',form = form, posts=posts, pagination=pagination, show_follow_posts=show_follow_posts)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_follow_posts', '', max_age=30*24*60*60)
    return resp

@main.route('/follow')
@login_required
def show_follow():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_follow_posts', '1', max_age=30*24*60*60)
    return resp


#show profile
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user:
        posts = user.post.order_by(Post.timestamp.desc()).all()
        #posts = Post.query.filter_by(author=user).all()
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.realname.data #update, not create new
        current_user.location = form.location.data
        current_user.about_me = form.aboutme.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('.user', username=current_user.username))
    form.realname.data = current_user.name
    form.location.data = current_user.location
    form.aboutme.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/post/<int:id>')
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post', id = post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):   
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You have removed a post.')
    return redirect(url_for('.index'))
    
@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()  
    current_user.following(user)  
    return redirect(url_for('.user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()  
    current_user.unfollowing(user)  
    return redirect(url_for('.user', username=username)) 

@main.route('/followers/<username>')
@login_required
def followers(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    pagination = user.followers.paginate(page,error_out=False) #retrun the list that conatins the obj
    follows = [{'user':item.followers, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html', endpoint='.followers', user=user,follows=follows, pagination=pagination)

@main.route('/followed/<username>')
@login_required
def followed(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first()
    pagination = user.followed.paginate(page,error_out=False)
    followed = [{'user':item.followed, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html',endpoint='.followed', user=user, follows=followed, pagination=pagination)

        


