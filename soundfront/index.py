from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
	album_frame = 365
	album_frame_string = request.args.get('album_frame') or 'year'
	if album_frame_string == 'year':
		album_frame = 365
	elif album_frame_string == 'month':
		album_frame = 30
	elif album_frame_string == 'week':
		album_frame = 7
	elif album_frame_string == 'day':
		album_frame = 1

	song_frame = 365
	song_frame_string = request.args.get('song_frame') or 'year'
	if song_frame_string == 'year':
		song_frame = 365
	elif song_frame_string == 'month':
		song_frame = 30
	elif song_frame_string == 'week':
		song_frame = 7
	elif song_frame_string == 'day':
		song_frame = 1	

	album_repo = current_app.config['album']
	user_repo = current_app.config['user']
	song_repo = current_app.config['song']

	cart = []

	if 'user_id' in session:
		user_id = session['user_id']
		cart_repo = current_app.config['cart']
		cart = cart_repo.list_cart(user_id)

	recent_albums = album_repo.list_albums(page=1, page_size=10)
	top_rated_albums = album_repo.get_top_rated_albums(frame=album_frame)
	top_rated_songs = song_repo.get_top_rated_songs(frame=song_frame)
	most_critical_users = user_repo.get_most_critical_users(count=6)

	return render_template('index.html', 
		top_rated_albums=top_rated_albums, 
		top_rated_songs=top_rated_songs, 
		recent_albums=recent_albums, 
		most_critical_users=most_critical_users, 
		song_frame=song_frame_string, 
		album_frame=album_frame_string,
		cart=cart)

@bp.route('/search', methods=['GET','POST'])
def search():
	album_repo = current_app.config['album']
	song_repo = current_app.config['song']

	search = request.form['searchform'] + '%'

	albums = album_repo.searchfor_album(search)
	songs = song_repo.search_for_song(search)

	searchtext = search[:-1]
	return render_template('search.html', albums=albums, songs=songs, searchtext=searchtext)