from flask import (Blueprint, render_template, current_app)
from .album import AlbumRepo

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
	album_repo = current_app.config['album']
	albums = album_repo.list_albums(page=1, page_size=5)
	return render_template('index.html', albums=albums)

