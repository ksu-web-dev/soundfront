from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('songs', __name__, url_prefix='/songs')


@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None:
        page = 1

    pagination_data = {}
    pagination_data['page'] = int(page)
    pagination_data['href'] = '/songs'
    pagination_data['add_button_text'] = 'Add a Song'

    cart = []

    if 'user_id' in session:
        user_id = session['user_id']
        cart_repo = current_app.config['cart']
        cart = cart_repo.list_cart(user_id)

    repo = current_app.config['song']
    songs = repo.list_song(page, 10)
    return render_template('songs/index.html', songs=songs, page=int(page), pagination_data=pagination_data, cart=cart)


@bp.route('/<song_id>', methods=['GET'])
def get(song_id):
    repo = current_app.config['song']
    song = repo.read_song(song_id)

    if song is None:
        return render_template('error.html', message='Song does not exist.')

    page = request.args.get('page')
    if page is None:
        page = 1

    ratings = repo.list_reviews(song.SongID, page, 10)
    tags = repo.list_tags(song.SongID)
    return render_template('songs/id.html', song=song, ratings=ratings, page=int(page), tags=tags)


@bp.route('/<song_id>/rate', methods=['GET', 'POST'])
def rate(song_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    repo = current_app.config['song']
    song = repo.read_song(song_id)

    if request.method == 'POST':
        rating = request.form['rating']
        review = request.form['review']

        if 'user_id' not in session:
            return render_template('error.html', message='Not logged in.')

        repo.rate_song(session['user_id'], song.SongID, rating, review)

        return redirect(url_for('songs.get', song_id=song.SongID))

    return render_template('songs/rate.html', song=song)


@bp.route('/new', methods=['GET', 'POST'])
def new():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        album = request.form['album'] or None
        price = request.form['price']
        length = request.form['length']
        description = request.form['description']

        error = None

        if not title:
            error = 'Title is required.'
        elif not price:
            error = 'Price is required.'
        elif not 'user_id' in session:
            return redirect(url_for('auth.login'))

        if error is None:
            repo = current_app.config['song']
            user_id = session['user_id']
            repo.insert_song(user_id, album, title, length, price, description)
            return redirect(url_for('songs.index'))

        flash(error)

    user_repo = current_app.config['user']
    albums = user_repo.list_albums(session['user_id'])

    return render_template('songs/new.html', albums=albums)


class SongRepo():
    def __init__(self, conn):
        self.conn = conn

    def insert_song(self, userid='', albumid=None, title='', length=0, price=0, description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.InsertSong
                @UserID=?,
	            @AlbumID=?,
	            @Title=?,
	            @Length=?,
	            @Price=?,
	            @Description=?
            """, userid, albumid, title, length, price, description)
        return cursor.fetchone()

    def update_song(self, songid='', title='', length='', price='', description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.UpdateSong
                @SongID=?,
	            @Title=?,
	            @Length=?,
	            @Price=?,
	            @Description=?
            """, songid, title, length, price, description)
        return cursor.fetchone()

    def read_song(self, songid):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadSong @SongID=?', songid)
        return cursor.fetchone()

    def delete_song(self, songid):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.DeleteSong @SongID=?', songid)

    def list_song(self, page, pagesize):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListSong @Page=?, @PageSize=?', page, pagesize)
        return cursor.fetchall()

    def list_reviews(self, song_id, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListSongRating @SongID=?, @Page=?, @PageSize=?', song_id, page, page_size)
        return cursor.fetchall()

    def list_tags(self, song_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListSongTags @SongID=?', song_id)
        return cursor.fetchall()


    def rate_song(self, user_id, song_id, rating=1, review_text=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.InsertSongRating
                @UserID=?,
                @SongID=?,
                @Rating=?,
                @ReviewText=?
        """, user_id, song_id, rating, review_text)
        return cursor.fetchone()
