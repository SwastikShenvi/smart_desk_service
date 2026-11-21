import hashlib
from domain.users import User
from domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError


class AuthService:
    """
    This is our Application layer class for handling login and signup.
    It does not know anything about JSON files directly, it just asks
    the user_repository to load or save users. This keeps responsibilities
    separated, the way the assignment wants.
    """

    def __init__(self, user_repository):
        """user_repository is injected from outside (Dependency Inversion),
        so AuthService does not need to know how users are actually stored"""
        self.user_repository = user_repository

    def hash_password(self, password):
        """
        We never store plain text passwords. Instead we convert the
        password into a fixed length scrambled string using SHA-256,
        so even if the JSON file is opened, the real password is not visible.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        """
        Creates a brand new user account.
        Checks all existing usernames first (case-insensitive) so that
        someone cannot sign up twice with the same name in different cases.
        """
        users = self.user_repository.load_users()

        for user in users:
            if user.username.lower() == username.lower():
                # username already taken, stop here with a clear error
                raise UserAlreadyExistsError(username)

        # only hash the password once we know the username is free
        new_user = User(username, self.hash_password(password))
        users.append(new_user)
        self.user_repository.save_users(users)
        return new_user

    def login(self, username, password):
        """
        Checks the entered username and password against our stored users.
        We hash the entered password first, then compare hashes,
        we never compare plain text passwords directly.
        """
        users = self.user_repository.load_users()
        hashed_password = self.hash_password(password)

        for user in users:
            if user.username.lower() == username.lower() and user.check_password(hashed_password):
                # username matched and password hash matched, login success
                return user

        # if we reach here, no matching user was found
        raise InvalidCredentialsError()
