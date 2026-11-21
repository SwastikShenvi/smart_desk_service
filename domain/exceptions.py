""" These are our own custom exceptions.
Python already gives us a built-in Exception class, but here we
create specific, meaningful error types so the rest of the app
can catch exactly what went wrong instead of guessing from a generic error message."""


class RequestNotFoundError(Exception):
    """
    Raised when someone searches or tries to resolve a request
    using a Request ID that does not exist in our data.
    """
    def __init__(self, request_id):
        # super() builds the normal Exception message for us
        super().__init__(f"No service request found with ID {request_id}.")
        self.request_id = request_id


class DuplicateRequestError(Exception):
    """
    Raised when someone tries to create a service request
    using a Request ID that already exists.
    """
    def __init__(self, request_id):
        super().__init__(f"A service request with ID {request_id} already exists.")
        self.request_id = request_id


class InvalidPriorityError(Exception):
    """
    Raised when the priority entered by the user is not
    one of the allowed values: LOW, MEDIUM, HIGH.
    """
    def __init__(self, priority):
        super().__init__("Priority must be LOW, MEDIUM or HIGH.")
        # storing the bad value the user actually typed
        self.priority = priority


class InvalidCredentialsError(Exception):
    """
    Raised during login when the username or password
    does not match what we have stored.
    """
    def __init__(self):
        super().__init__("Invalid username or password. Please try again.")


class UserAlreadyExistsError(Exception):
    """
    Raised during signup/registration when someone tries
    to create an account with a username that is already taken.
    """
    def __init__(self, username):
        super().__init__(f"Username {username} is already taken. Please choose another one.")
        self.username = username
