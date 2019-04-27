from flask import (Blueprint, render_template, current_app, request)

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
	frame = request.args.get('frame')
	if frame == 'year' or frame is None:
		frame = 365
	elif frame == 'month':
		frame = 30
	elif frame == 'week':
		frame = 7
	elif frame == 'day':
		frame = 1

	album_repo = current_app.config['album']
	user_repo = current_app.config['user']

	recent_albums = album_repo.recent_albums(page=1, page_size=10)
	top_rated_albums = album_repo.get_top_rated_albums(frame=frame)
	most_critical_users = user_repo.get_most_critical_users(count=6)

	return render_template('index.html', top_rated_albums=top_rated_albums, most_critical_users=most_critical_users, recent_albums=recent_albums)
