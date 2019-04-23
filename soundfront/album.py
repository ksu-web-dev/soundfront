from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None: page = 1

    pagination_data = {}
    pagination_data['page'] = int(page)
    pagination_data['href'] = '/albums'
    pagination_data['add_button_text'] = 'Add an Album'
    
    album_repo = current_app.config['album']
    albums = album_repo.recent_albums(page=page, page_size=15)
    return render_template('albums/index.html', albums=albums, pagination_data=pagination_data)

@bp.route('/<album_id>', methods=['GET'])
def album(album_id):
    album_repo = current_app.config['album']
    album_songs = album_repo.list_songs(album_id)
    # TODO: Add check for when the album_id is not found.
    return render_template('albums/album.html', album_songs=album_songs)

@bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        user_id = session['user_id']
        title = request.form['title']
        length = request.form['length']
        price = request.form['price']
        description = request.form['description']

        error = None

        if not title:
            error = 'Title is required'
        elif not price:
            error = 'Price is required'
        elif not user_id:
            return redirect(url_for('auth.login'))

        if error is None:
            album_repo = current_app.config['album']
            album_repo.create_album(user_id, title, length, price, description)
            return redirect(url_for('albums.index')) 

        flash(error)

    return render_template('albums/new.html')

class AlbumRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_album(self, user_id='', album_title='', album_length='', album_price='', album_description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
        EXEC Soundfront.CreateAlbum
            @AlbumUserId=?,
            @AlbumTitle=?,
            @AlbumLength=?,
            @AlbumPrice=?,
            @AlbumDescription=?
            """, user_id, album_title, album_length, album_price, album_description)
        return cursor.fetchone()

    def list_songs(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetAlbumSongs @AlbumId=?', album_id)
        return cursor.fetchall()

    def get_album(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadAlbum @AlbumAlbumId=?', album_id)
        return cursor.fetchone()

    def list_albums(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ListAlbums
                @Page=?,
                @pageSize=?
            """, page, page_size)

        return cursor.fetchall()

    def recent_albums(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.RecentAlbums
                @Page=?,
                @PageSize=?
            """, page, page_size)

        return cursor.fetchall()

    