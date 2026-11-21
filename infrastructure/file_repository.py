"""This class handles all the JSON reading and writing for service
requests. Keeping this separate from ServiceRequest means our
domain class stays clean, and if we ever swap JSON for a real
database later, this is the only file we'd need to change.
"""
"""
This is our infrastructure layer for service requests. It's the only
place in the app that actually touches the file system and JSON.
It knows how to convert between ServiceRequest objects and the plain
dictionaries stored in requests.json, so the service layer never has
to worry about file handling itself.
"""
import json
import os
from domain.service_request import ServiceRequest


class FileRepository:
    def __init__(self, file_path="data/requests.json"):
        """
        Sets up the path to the data file. Creates the folder and
        the file itself (with an empty list) if they don't exist yet,
        so the rest of the app never has to worry about missing files.
        """
        self.file_path = file_path
        folder = os.path.dirname(self.file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def load_requests(self):
        """
        Reads the JSON file and converts every entry back into a
        ServiceRequest object. Returns an empty list if the file is
        empty or contains invalid JSON, instead of crashing the app.
        """
        if os.path.getsize(self.file_path) == 0:
            return []
        with open(self.file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return []
        requests = []
        for item in data:
            request = ServiceRequest(
                item["request_id"],
                item["employee_name"],
                item["issue"],
                item["priority"],
                item["status"]
            )
            requests.append(request)
        return requests

    def save_requests(self, requests):
        """
        Converts every ServiceRequest object back into a dictionary
        and writes the whole list to the JSON file, overwriting
        whatever was there before.
        """
        data = []
        for request in requests:
            data.append(request.to_dict())
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)