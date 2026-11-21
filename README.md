#Smart Service Desk Management System
##Problem Statement
A company receives IT support requests from employees for laptop, software, network, password, account, and access related issues. These were tracked manually. This application gives support staff a simple, login-protected CLI tool to create, view, search, and resolve service requests, with all data kept safe in JSON files between runs.

Features Implemented
Register and login before the main menu is shown
Create a service request (status is always set to OPEN automatically)
Block duplicate Request IDs with a friendly message
View all saved service requests
Search a request by Request ID
Resolve an OPEN request; show a message if it is already RESOLVED
Full persistence: requests and users reload correctly after restart
Concepts Used
OOP: ServiceRequest and User classes with constructors, attributes, and methods (resolve(), check_password())
Exception Handling: custom exceptions (RequestNotFoundError, DuplicateRequestError, InvalidPriorityError, InvalidCredentialsError, UserAlreadyExistsError), no bare except
File Handling: JSON persistence through the os and json modules in the infrastructure layer
SOLID: Single Responsibility (each class/module has one job) and Dependency Inversion (services depend on repository objects passed into them, not on file details)
DDD: domain / application / infrastructure layers kept strictly separate
Git: development branch for building features, merged into main after testing
Project Folder Structure
smart-service-desk/
├── domain/
│   ├── service_request.py
│   ├── users.py
│   └── exceptions.py
├── application/
│   ├── request_service.py
│   └── auth_service.py
├── infrastructure/
│   ├── file_repository.py
│   └── user_repository.py
├── data/
│   ├── requests.json
│   └── users.json
├── main.py
├── README.md
└── .gitignore
