from flask import render_template, redirect, url_for, flash, request, Blueprint,abort
from app.posts.forms import AddPostForm, EditPostForm
from models import Post
from app.helper import add_image
from flask_login import login_required

posts_blueprint = Blueprint("posts", __name__, template_folder="templates/")

@posts_blueprint.route('/get-posts')
@login_required
def get_posts(): 
    posts = Post.get_posts()
    return render_template("posts.html", posts=posts)


@posts_blueprint.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        image_data = form.image.data
        image_file_path = add_image(image_data)
        post = Post(form.title.data, form.author.data,
                    form.body.data, image_file_path)
        post.add_post()
        return redirect(url_for('posts.get_posts'))
    flash('Internal Server Error')
    return render_template('create.html', form=form)


@posts_blueprint.route('/edit-post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.get_post(id)
    if post == None:
        abort(404)


    form = EditPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.image.data:
            image_data = form.image.data
            image_file_path =  add_image(image_data)
        else:
            image_file_path = post[4]
        post = Post(id=post[0], title=form.title.data, author=form.author.data,
                    body=form.body.data, image=image_file_path)
        post.edit_post()
        return redirect(url_for('posts.get_posts'))
    elif request.method == 'GET':
        form.title.data = post[1]
        form.author.data = post[2]
        form.body.data = post[3]
        form.image.process_data(post[4])

    flash('Internal Server Error')
    return render_template('edit.html', form=form)

