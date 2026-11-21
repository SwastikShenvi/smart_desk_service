"""
This is the application layer for service requests.
It  coordinates between the domain object (ServiceRequest) and the
infrastructure (FileRepository). Think of each method here as
one "use case" the assignment asks for.
"""
from domain.service_request import ServiceRequest
from domain.exceptions import DuplicateRequestError, RequestNotFoundError


class RequestService:
    def __init__(self, file_repository):
        #Stores the repository we'll use to load and save requests.
        self.file_repository = file_repository

    def create_request(self, request_id, employee_name, issue, priority):
        """
        Creates a new service request after making sure no other
        request already exists with the same ID (case-insensitive).
        Saves the updated list back to the file and returns the new request.
        """
        requests = self.file_repository.load_requests()
        for request in requests:
            if request.request_id.upper() == request_id.upper():
                raise DuplicateRequestError(request_id)
        new_request = ServiceRequest(request_id, employee_name, issue, priority)
        requests.append(new_request)
        self.file_repository.save_requests(requests)
        return new_request

    def view_requests(self):
        """Returns every service request currently saved."""
        return self.file_repository.load_requests()

    def search_request(self, request_id):
        """
        Looks through all requests for one matching the given ID
        (case-insensitive). Raises an error if nothing is found.
        """
        requests = self.file_repository.load_requests()
        for request in requests:
            if request.request_id.upper() == request_id.upper():
                return request
        raise RequestNotFoundError(request_id)

    def resolve_request(self, request_id):
        """
        Finds the request with the given ID and marks it as resolved.
        Saves the change to file and returns the request along with
        a flag telling whether it was resolved just now or already
        was resolved before. Raises an error if the ID doesn't exist.
        """
        requests = self.file_repository.load_requests()
        for request in requests:
            if request.request_id.upper() == request_id.upper():
                resolved_now = request.resolve()
                self.file_repository.save_requests(requests)
                return request, resolved_now
        raise RequestNotFoundError(request_id)