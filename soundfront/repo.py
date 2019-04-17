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
        """, 1, email, display_name, password)
        return cursor.fetchone()

    def get_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetUser @UserID=?', id)
        return cursor.fetchone()