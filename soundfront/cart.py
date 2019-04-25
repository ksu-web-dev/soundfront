from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None: page = 1

    cart = repo.read_cart(session['user_id'])
    
    return render_template('cart/index.html', cart=cart, page=int(page))

class CartRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_cart(self, userid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.CreateCart @UserID=?', userid)
        return cursor.fetchone()

    def read_cart(self, userid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadCart @UserID=?', userid)
        return cursor.fetchone()

    def insert_songcart(self, songid='', cartid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.InsertSongCart @SongID=? @CartID=?', songid, cartid)
        return cursor.fetchone()

    def delete_songcart(self, songcartid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.DeleteSongCart @SongCartID=?', songcartid)
        return cursor.fetchone()

    def read_songcart(self, songcartid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadSongCart @SongCartID=?', songcartid)
        return cursor.fetchone()

    def list_songcart(self, page='', pagesize=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ListSongCart @Page=? @PageSize=?', page, pagesize)
        return cursor.fetchone()

    def insert_albumcart(self, albumid='', cartid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.InsertAlbumCart @AlbumID=? @CartID=?', albumid, cartid)
        return cursor.fetchone()

    def delete_albumcart(self, albumcartid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.DeleteAlbumCart @AlbumCartID=?', albumcartid)
        return cursor.fetchone()

    def read_albumcart(self, albumcartid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadAlbumCart @AlbumCartID=?', albumcartid)
        return cursor.fetchone()

    def list_albumcart(self, page='', pagesize=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ListAlbumCart @Page=? @PageSize=?', page, pagesize)
        return cursor.fetchone()
