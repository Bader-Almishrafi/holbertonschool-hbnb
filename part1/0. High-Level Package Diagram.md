# HBnB Evolution – Part 1: Technical Documentation

## Overview
This repository contains the first phase of the **HBnB Evolution** project.  
The goal of this part is to design and document the system architecture before starting the implementation.

The documentation focuses on defining a clear structure for the application using UML diagrams, ensuring proper separation of concerns and a solid foundation for future development stages.

---

## Architecture Overview
The HBnB application follows a **three-layer architecture**:

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

The communication between layers is organized using the **Facade design pattern**, which provides a unified interface and reduces coupling between components.

---

## High-Level Package Diagram
The following diagram illustrates the overall structure of the application and the interaction between its layers.

![High-Level Package Diagram](./0.%20High-Level%20Package%20Diagram.png)

### Layer Responsibilities

#### Presentation Layer
Handles user interaction through APIs and services.  
This layer receives requests, forwards them to the Business Logic layer via the Facade, and returns responses to the user.

#### Business Logic Layer
Contains the core application logic and domain models:
- User
- Place
- Review
- Amenity

This layer enforces business rules and coordinates operations between entities.

#### Persistence Layer
Manages data storage and retrieval.  
It includes repositories and database access components responsible for performing CRUD operations while remaining isolated from the upper layers.

---

## Design Pattern
### Facade Pattern
The Facade pattern is used to simplify communication between the Presentation Layer and the Business Logic Layer by exposing a single unified interface.  
This approach improves maintainability, readability, and scalability of the system.
