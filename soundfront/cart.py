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

        item_type = request.form['type']

        if item_type == 'Song':
            song_id = request.form['songid']
            repo.add_song_to_cart(song_id, cart.CartID)
        elif item_type == 'Album':
            album_id = request.form['albumid']
            repo.add_album_to_cart(album_id, cart.CartID)

        return redirect(request.url)

    ordertotal = repo.cart_total_price(user_id)
    return render_template('cart/index.html', cart=cart_items, ordertotal=ordertotal)


@bp.route('/checkout')
def checkout():
    repo = current_app.config['cart']

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    print(repo.cart_total_price(user_id))
    if repo.cart_total_price(user_id)[0] is None:
        return redirect(url_for('cart.index'))

    cart_items = repo.list_cart(user_id)

    if request.method == 'POST':
        cart = repo.get_cart(user_id)
        song_id = request.form['songid']
        repo.add_song_to_cart(song_id, cart.CartID)

        return redirect(request.url)

    ordertotal = repo.cart_total_price(user_id)
    return render_template('cart/checkout.html', cart=cart_items, ordertotal=ordertotal)


@bp.route('/confirmation')
def confirmation():
    repo = current_app.config['cart']

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    if repo.cart_total_price(user_id)[0] is None:
        return redirect(url_for('cart.index'))

    cart_items = repo.list_cart(user_id)
    cartID = repo.get_cart(user_id)
    ordertotal = repo.cart_total_price(user_id)
    repo.clear_song_cart(cartID.CartID)
    repo.clear_album_cart(cartID.CartID)

    if request.method == 'POST':
        cart = repo.get_cart(user_id)
        song_id = request.form['songid']
        repo.add_song_to_cart(song_id, cart.CartID)

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

    def add_song_to_cart(self, song_id, cart_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC SoundFront.AddSongToCart @SongID=?, @CartID=?', song_id, cart_id)
        return True

    def clear_song_cart(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ClearSongCart @CartID=?', cart_id)

    def add_album_to_cart(self, album_id, cart_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.AddAlbumToCart @AlbumID=?, @CartID=?', album_id, cart_id)

    def clear_album_cart(self, cart_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ClearAlbumCart @CartID=?', cart_id)

    def cart_total_price(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.CartTotalPrice @UserID=?', user_id)
        return cursor.fetchone()
