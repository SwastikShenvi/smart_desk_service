"""
This is our domain model for a user. It's a plain data class that
just knows how to hold a username and a hashed password, check a
password match, and convert itself to a dictionary for saving to
JSON. It doesn't know anything about files or hashing algorithms,
that's handled elsewhere (AuthService and UserRepository).
"""
class User:
    def __init__(self, username, password_hash):
        """Stores the username and the already-hashed password."""
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password_hash):
        """
        Compares the given hashed password with the one stored on
        this user. Returns True if they match, False otherwise.
        """
        return self.password_hash == password_hash

    def to_dict(self):
        """Converts this user into a plain dictionary for JSON storage."""
        return {
            "username": self.username,
            "password_hash": self.password_hash
        }