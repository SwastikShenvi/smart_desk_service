"""
This is the domain layer's core model: a ServiceRequest.
It represents a single service desk ticket and knows how to validate
its own data (like priority) and how to resolve itself. It has no
idea how it gets saved to a file or shown on screen, that's for
other layers to handle.
"""
from domain.exceptions import InvalidPriorityError


class ServiceRequest:
    def __init__(self, request_id, employee_name, issue, priority, status="OPEN"):
        """
        Creates a new service request. Validates that priority is
        one of LOW, MEDIUM or HIGH before accepting it and defaults
        status to OPEN unless specified otherwise.
        """
        if priority.upper() not in ["LOW", "MEDIUM", "HIGH"]:
            raise InvalidPriorityError(priority)
        self.request_id = request_id
        self.employee_name = employee_name
        self.issue = issue
        self.priority = priority.upper()
        self.status = status

    def resolve(self):
        """
        Marks the request as RESOLVED.
        Returns True if it just got resolved now, or False if it
        was already resolved before, so the caller knows what happened.
        """
        if self.status == "RESOLVED":
            return False
        self.status = "RESOLVED"
        return True

    def to_dict(self):
        """Converts the request into a plain dictionary, handy for saving to JSON."""
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status
        }

    def __str__(self):
        """Gives a readable, single-line summary of the request for printing."""
        return f"{self.request_id} | {self.employee_name} | {self.issue} | {self.priority} | {self.status}"