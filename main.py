"""
This is the entry point of the whole app, our presentation layer.
It just talks to the user: shows menus, takes input and calls
the application services. It never opens a file or touches JSON
directly, that's not its job.
"""
from application.request_service import RequestService
from application.auth_service import AuthService
from infrastructure.file_repository import FileRepository
from infrastructure.user_repository import UserRepository
from domain.exceptions import (
    DuplicateRequestError,
    RequestNotFoundError,
    InvalidPriorityError,
    InvalidCredentialsError,
    UserAlreadyExistsError
)


def login_menu(auth_service):
    """
    Shows the login/register menu in a loop until the user either
    logs in successfully or chooses to exit.
    Returns the logged-in user object, or None if the user exits.
    """
    while True:
        print("\nSMART SERVICE DESK - LOGIN")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # Ask for credentials and try to log the user in
            username = input("Enter Username: ").strip()
            password = input("Enter Password: ").strip()
            try:
                user = auth_service.login(username, password)
                print(f"Welcome, {user.username}!")
                return user
            except InvalidCredentialsError as error:
                print(error)

        elif choice == "2":
            # Ask for new credentials and try to register a new user
            username = input("Choose a Username: ").strip()
            password = input("Choose a Password: ").strip()
            try:
                auth_service.register(username, password)
                print("Registration successful. Please login now.")
            except UserAlreadyExistsError as error:
                print(error)

        elif choice == "3":
            # User chosoe to exit before logging in
            return None

        else:
            print("Invalid input. Please choose between 1 and 3.")


def show_menu():
    """Prints the main menu options once the user is logged in."""
    print("\nSMART SERVICE DESK SYSTEM")
    print("1. Create Service Request")
    print("2. View All Requests")
    print("3. Search Request")
    print("4. Resolve Request")
    print("5. Exit")


def create_request(request_service):
    """
    Collects request details from the user and asks the request
    service to create a new service request. Handles duplicate ID
    and invalid priority errors gracefully.
    """
    request_id = input("Enter Request ID: ").strip()
    employee_name = input("Enter Employee Name: ").strip()
    issue = input("Enter Issue: ").strip()
    priority = input("Enter Priority: ").strip()
    try:
        request_service.create_request(request_id, employee_name, issue, priority)
        print("Service Request created successfully.")
    except DuplicateRequestError as error:
        print(error)
    except InvalidPriorityError as error:
        print(error)


def view_requests(request_service):
    """Fetches and prints every service request currently stored."""
    requests = request_service.view_requests()
    if not requests:
        print("No service requests found.")
        return
    for request in requests:
        print(request)


def search_request(request_service):
    """
    Asks the user for a request ID and prints the matching request,
    or an error message if nothing is found.
    """
    request_id = input("Enter Request ID to search: ").strip()
    try:
        request = request_service.search_request(request_id)
        print(request)
    except RequestNotFoundError as error:
        print(error)


def resolve_request(request_service):
    """
    Asks the user for a request ID and marks it as resolved.
    Prints a different message depending on whether it was just
    resolved now or was already resolved earlier.
    """
    request_id = input("Enter Request ID to resolve: ").strip()
    try:
        request, resolved_now = request_service.resolve_request(request_id)
        if resolved_now:
            print(f"{request.request_id} marked as RESOLVED.")
        else:
            print(f"{request.request_id} is already RESOLVED.")
    except RequestNotFoundError as error:
        print(error)


def main():
    """
    The main driver function. Logs the user in first, then keeps
    showing the menu and routing the user's choice to the right
    function until they decide to exit.
    """
    auth_service = AuthService(UserRepository())
    user = login_menu(auth_service)

    if user is None:
        print("Goodbye!")
        return

    request_service = RequestService(FileRepository())

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_request(request_service)
        elif choice == "2":
            view_requests(request_service)
        elif choice == "3":
            search_request(request_service)
        elif choice == "4":
            resolve_request(request_service)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()