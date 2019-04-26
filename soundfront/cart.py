from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('cart', __name__, url_prefix='/cart')


@bp.route('/', methods=['GET', 'POST'])
def index():
    repo = current_app.config['cart']

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_items = repo.list_cart(user_id)

    if request.method == 'POST':
        cart = repo.get_cart(user_id)
        song_id = request.form['songid']
        repo.insert_songcart(song_id, cart.CartID)

        return redirect(request.url)

    ordertotal = repo.cart_total_price(user_id)
    return render_template('cart/index.html', cart=cart_items, ordertotal=ordertotal)

@bp.route('/checkout')
def checkout():
    repo = current_app.config['cart']

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_items = repo.list_cart(user_id)

    if request.method == 'POST':
        cart = repo.get_cart(user_id)
        song_id = request.form['songid']
        repo.insert_songcart(song_id, cart.CartID)

        return redirect(request.url)

    ordertotal = repo.cart_total_price(user_id)
    return render_template('cart/checkout.html', cart=cart_items, ordertotal=ordertotal)

@bp.route('/confirmation')
def confirmation():
    repo = current_app.config['cart']

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_items = repo.list_cart(user_id)
    cartID = repo.get_cart(user_id)
    ordertotal = repo.cart_total_price(user_id)
    repo.delete_songcart(cartID.CartID)
    repo.delete_albumcart(cartID.CartID)

    if request.method == 'POST':
        cart = repo.get_cart(user_id)
        song_id = request.form['songid']
        repo.insert_songcart(song_id, cart.CartID)

        return redirect(request.url)

    return render_template('cart/confirmation.html', cart=cart_items, ordertotal=ordertotal)

class CartRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_cart(self, userid=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.CreateCart @UserID=?', userid)
        return cursor.fetchone()

    def get_cart(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetCart @UserID=?', user_id)
        return cursor.fetchone()

    def list_cart(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ListCart @UserID=?', user_id)
        return cursor.fetchall()

    def insert_songcart(self, songid='', cartid=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC SoundFront.InsertSongCart @SongID=?, @CartID=?', songid, cartid)
        return True

    def delete_songcart(self, cartid=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.DeleteSongCart @CartID=?', cartid)

    def read_songcart(self, songcartid=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ReadSongCart @SongCartID=?', songcartid)
        return cursor.fetchone()

    def list_songcart(self, page='', pagesize=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListSongCart @Page=? @PageSize=?', page, pagesize)
        return cursor.fetchone()

    def insert_albumcart(self, albumid='', cartid=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.InsertAlbumCart @AlbumID=? @CartID=?', albumid, cartid)
        return cursor.fetchone()

    def delete_albumcart(self, cartid=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.DeleteAlbumCart @CartID=?', cartid)

    def read_albumcart(self, albumcartid=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ReadAlbumCart @AlbumCartID=?', albumcartid)
        return cursor.fetchone()

    def list_albumcart(self, page='', pagesize=''):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListAlbumCart @Page=? @PageSize=?', page, pagesize)
        return cursor.fetchone()

    def cart_total_price(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.CartTotalPrice @UserID=?', user_id)
        return cursor.fetchone()
