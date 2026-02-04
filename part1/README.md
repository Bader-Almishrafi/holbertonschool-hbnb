High-Level Package Diagram – HBnB Application

This diagram presents a high-level architectural overview of the HBnB application based on a three-layer architecture. The design clearly separates responsibilities across layers and uses the Facade pattern to simplify communication between them.

Presentation Layer

The Presentation Layer represents the entry point of the application and handles all interactions with users. It includes:

Services / APIs responsible for receiving client requests and returning responses.

Basic request handling and data transfer.

This layer does not contain business rules. Instead, it communicates with the Business Logic Layer exclusively through the Facade pattern, ensuring a clean separation of concerns.

Business Logic Layer

The Business Logic Layer contains the core logic of the application and represents the central part of the system. It includes:

A Model component that manages application behavior.

Core entities: User, Place, Review, and Amenity.

This layer enforces all business rules and coordinates operations between entities before interacting with the Persistence Layer.

Persistence Layer

The Persistence Layer is responsible for data storage and retrieval. It includes:

Repositories and database access components.

Direct communication with the database to perform CRUD operations.

This layer is isolated from the Presentation Layer, ensuring that data access concerns remain independent from user interaction logic.

Facade Pattern

The Facade pattern acts as a unified interface between the Presentation Layer and the Business Logic Layer. It reduces coupling between layers, improves maintainability, and provides a clear and structured flow of data across the system.