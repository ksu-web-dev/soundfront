from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('albums', __name__, url_prefix='/albums')


@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None:
        page = 1

    pagination_data = {}
    pagination_data['page'] = int(page)
    pagination_data['href'] = '/albums'
    pagination_data['add_button_text'] = 'Add an Album'
    pagination_data['include_next_button'] = True

    album_repo = current_app.config['album']
    albums = album_repo.recent_albums(page=page, page_size=15)

    return render_template('albums/index.html', albums=albums, pagination_data=pagination_data)

@bp.route('/<album_id>', methods=['GET'])
def get(album_id):
    album_repo = current_app.config['album']
    album = album_repo.get_album(album_id)
    album_songs = album_repo.list_songs(album_id)
    # TODO: Add check for when the album_id is not found.

    cart = []

    if 'user_id' in session:
        user_id = session['user_id']
        cart_repo = current_app.config['cart']
        cart = cart_repo.list_cart(user_id)

    return render_template('albums/id.html', album_songs=album_songs, album=album, cart=cart)

@bp.route('/new', methods=['GET', 'POST'])
def new():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        user_id = session['user_id']
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        error = None

        if not title:
            error = 'Title is required'
        elif not price:
            error = 'Price is required'

        if error is None:
            album_repo = current_app.config['album']
            album_repo.create_album(user_id, title, price, description)
            return redirect(url_for('albums.index'))

        flash(error)

    return render_template('albums/new.html')

@bp.route('/<album_id>/rate', methods=['GET', 'POST'])
def rate(album_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    repo = current_app.config['album']
    album = repo.get_album(album_id)

    if request.method == 'POST':
        rating = request.form['rating']
        review = request.form['review']

        if 'user_id' not in session:
            return render_template('error.html', message='Not logged in.')

        repo.rate_album(session['user_id'], album.AlbumID, rating, review)

        return redirect(url_for('albums.get', album_id=album.AlbumID))

    return render_template('albums/rate.html', album=album)

class AlbumRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_album(self, user_id='', album_title='', album_art='', album_price='', album_description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
        EXEC Soundfront.CreateAlbum
            @AlbumUserId=?,
            @AlbumTitle=?,
            @AlbumAlbumArt=?,
            @AlbumPrice=?,
            @AlbumDescription=?
            """, user_id, album_title, album_art, album_price, album_description)

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

    def get_top_rated_albums(self, frame):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetTopRatedAlbums @TimeFrameInDays=?', frame)
        return cursor.fetchall()

    def recent_albums(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.RecentAlbums
                @Page=?,
                @PageSize=?
            """, page, page_size)

        return cursor.fetchall()

    def rate_album(self, user_id, album_id, rating, review_text):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.InsertAlbumRating
                @UserID=?,
                @AlbumID=?,
                @Rating=?,
                @ReviewText=?
            """, user_id, album_id, rating, review_text)
        return cursor.fetchone()


    def delete_album(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.DeleteAlbum
                @AlbumID=?
            """, album_id)
        return cursor.fetchone()

    def searchfor_album(self, page, page_size, search):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.SearchForAlbum
            @Page=?,
            @PageSize=?,
            @Search=?
            """, page, page_size, search)
        return cursor.fetchone()
