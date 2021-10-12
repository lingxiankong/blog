from flask import Flask, render_template, request, url_for, flash, redirect
from oslo_config import cfg
from oslo_db import options as db_options

from blog.db import api as db_api

CONF = cfg.CONF

opt_port = cfg.IntOpt(
    'port',
    default=5000,
)
CONF.register_cli_opts([opt_port])

opt_cosmos_endpoint = cfg.StrOpt(
    'endpoint',
    help='The URI of the Azure Cosmos DB account.'
)
opt_cosmos_key = cfg.StrOpt(
    'key',
    help='The primary of secondary key of the Azure Cosmos DB account.'
)
opt_group_cosmosdb = cfg.OptGroup('cosmosdb', title='Cosmos DB options')
CONF.register_group(opt_group_cosmosdb)
CONF.register_opts([opt_cosmos_endpoint, opt_cosmos_key], opt_group_cosmosdb)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['FLASK_ENV'] = 'development'


def get_post(post_id):
    post = db_api.get_post(post_id)
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    posts = db_api.get_posts()
    return render_template('index.html', posts=posts)


@app.route('/<post_id>')
def post(post_id):
    post = db_api.get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            db_api.create_post(title, content)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            db_api.update_post(id, title, content)
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    db_api.delete_post(id)
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


def main():
    CONF(args=None, project='blog', validate_default_values=False)
    db_options.set_defaults(CONF)
    # Register database config group.
    db_api.setup_db()
    app.run(host='0.0.0.0', port=CONF.port)


if __name__ == '__main__':
    main()
