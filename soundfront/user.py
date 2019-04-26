from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None:
        page = 1

    pagination_data = {}
    pagination_data['page'] = int(page)
    pagination_data['href'] = '/users'

    repo = current_app.config['user']
    users = repo.list_users(page, 10)
    user_count = repo.user_count()

    return render_template('users/index.html', users=users, current_page=int(page), user_count=user_count, pagination_data=pagination_data)


@bp.route('/<user_id>', methods=['GET'])
def profile(user_id):
    repo = current_app.config['user']
    user = repo.get_user(user_id)

    if user is None:
        return render_template('error.html', message='User does not exist')

    songs = repo.list_songs(user_id)
    albums = repo.list_albums(user_id)
    followers = repo.list_followers(user_id)
    following = repo.list_following(user_id)

    cart = []

    if 'user_id' in session:
        user_id = session['user_id']
        cart_repo = current_app.config['cart']
        cart = cart_repo.list_cart(user_id)

    return render_template('users/id.html', user=user, songs=songs, albums=albums, cart=cart, followers=followers, following=following)


class UserRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, email='', display_name='', password=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.CreateUser
                @Privacy=?,
                @DisplayName=?,
                @Email=?,
                @EnteredPassword=?
        """, 1, display_name, email, password)
        user = cursor.fetchone()
        cursor.execute('EXEC Soundfront.CreateCart @UserID=?', user.UserID)

        return user

    def check_login(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.CheckLogin @Email=?, @EnteredPassword=?', email, password)
        return cursor.fetchone()

    def list_users(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListUser @Page=?, @PageSize=?', page, page_size)
        return cursor.fetchall()

    def list_songs(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListSongsByUser @UserID=?', user_id)
        return cursor.fetchall()

    def list_albums(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'EXEC Soundfront.ListAlbumsByUser @UserID=?', user_id)
        return cursor.fetchall()

    def user_count(self):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.UserCount')
        return cursor.fetchone()[0]

    def get_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetUser @UserID=?', id)
        return cursor.fetchone()

    def get_user_by_email(self, email):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetUserByEmail @Email=?', email)
        return cursor.fetchone()

    def remove_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.RemoveUser @UserID=?', id)

    def follow_user(self, follower_user_id, followee_user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.FollowUser
                @FollowerUserID=?,
                @FolloweeUserID=?
            """, follower_user_id, followee_user_id)
        return cursor.fetchone()

    # pass in the id of the user page being viewed
    def list_followers(self, followee_user_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ListFollowers @FolloweeUserID=?', followee_user_id)
        return cursor.fetchall()

    # pass in the id of the user page being viewed
    def list_following(self, follower_user_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ListFollowing @FollowerUserID=?', follower_user_id)
        return cursor.fetchall()
