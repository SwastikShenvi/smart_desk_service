
"""
This is the infrastructure layer for users. Just like FileRepository
handles requests.json, this class is the only place that touches
users.json. It converts between User objects and plain dictionaries
so the auth service never has to deal with file handling directly.
"""
import json
import os
from domain.users import User


class UserRepository:
    def __init__(self, file_path="data/users.json"):
        """
        Sets up the path to the users data file. Creates the folder
        and the file itself (with an empty list) if they don't exist
        yet, so the app never crashes due to a missing file.
        """
        self.file_path = file_path
        folder = os.path.dirname(self.file_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)

    def load_users(self):
        """
        Reads the JSON file and converts every entry back into a
        User object. Returns an empty list if the file is empty or
        contains invalid JSON, instead of crashing the app.
        """
        if os.path.getsize(self.file_path) == 0:
            return []
        with open(self.file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return []
        users = []
        for item in data:
            user = User(item["username"], item["password_hash"])
            users.append(user)
        return users

    def save_users(self, users):
        """
        Converts every User object back into a dictionary and writes
        the whole list to the JSON file, overwriting whatever was
        there before.
        """
        data = []
        for user in users:
            data.append(user.to_dict())
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)