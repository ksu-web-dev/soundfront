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
    pagination_data['href'] = '/albums'
    pagination_data['add_button_text'] = 'Add an Album'

    repo = current_app.config['user']
    users = repo.list_users(page, 10)
    user_count = repo.user_count()
    return render_template('users/index.html', users=users, current_page=int(page), user_count=user_count)


@bp.route('/<user_id>', methods=['GET'])
def profile(user_id):
    repo = current_app.config['user']
    user = repo.get_user(user_id)

    if user is None:
        return render_template('error.html', message='User does not exist')

    songs = repo.list_songs(user_id)
    albums = repo.list_albums(user_id)

    return render_template('users/profile.html', user=user, songs=songs, albums=albums)


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
