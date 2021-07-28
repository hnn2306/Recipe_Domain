class User:
    def __init__(self, username, password, ID):
        self.username = username
        self.password = password
        self.ID = ID

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def __str__(self) -> str:
        return "User {username: " + self.username + ", password: " + self.password + ", ID: " + str(self.ID)
