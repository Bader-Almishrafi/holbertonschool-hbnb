# HBnB Evolution – Technical Documentation (Part 1)

## Overview
This document provides the technical documentation for **Part 1** of the HBnB Evolution project.
The objective of this phase is to define and document the system architecture, business logic design,
and API interaction flows before starting the implementation.

---

## Architecture Overview

The HBnB application follows a **three-layer architecture** designed to ensure separation of concerns,
maintainability, and scalability.

### Layers
- **Presentation Layer**: Handles user interaction through APIs and services.
- **Business Logic Layer**: Contains the core domain models and business rules.
- **Persistence Layer**: Manages data storage and retrieval.

Communication between layers is organized using the **Facade design pattern**.

---

## High-Level Package Diagram

![High-Level Package Diagram](./part1/0.%20High-Level%20Package%20Diagram.png)

### Description
This diagram illustrates the overall structure of the application and how responsibilities are distributed across layers.
The Presentation Layer communicates with the Business Logic Layer exclusively through a Facade,
which prevents direct coupling with the Persistence Layer.

---

## Business Logic Layer Design

![Business Logic Class Diagram](./part1/1.%20Detailed%20Class%20Diagram%20for%20Business%20Logic%20Layer.drawio.png)

### Core Entities

#### User
Represents application users and manages user-related data such as profile information and ownership of places and reviews.

#### Place
Represents properties listed in the application, including pricing, location, and ownership details.

#### Review
Represents feedback submitted by users for places, linking users and places together.

#### Amenity
Represents features that can be associated with places and reused across the system.

### Design Notes
- All entities use **UUID4** as a unique identifier.
- Creation and update timestamps are included for auditing purposes.
- Entity relationships reflect real-world constraints and system requirements.

---

## API Interaction Flow

Sequence diagrams illustrate how API requests move through the system layers and how components interact during execution.

---

### Fetching a List of Places

![Fetching a List of Places](./part1/Fetching%20a%20List%20of%20Places.drawio.png)

**Explanation**  
The user requests a list of available places through the Presentation Layer.
The request is processed by the Business Logic Layer and data is retrieved from the Persistence Layer
before being returned to the user.

---

### Place Creation

![Place Creation](./part1/Place%20Creation.drawio.png)

**Explanation**  
The user submits place data through the API.
The Business Logic Layer validates the input and persists the data through the Persistence Layer.

---

### Review Submission

![Review Submission](./part1/Review%20Submission.drawio.png)

**Explanation**  
A review is submitted for a specific place.
Validation occurs in the Business Logic Layer before the review is stored and confirmation is returned.

---

### User Registration

![User Registration](./part1/User%20Registration.drawio.png)

**Explanation**  
User registration data is validated and stored using the defined layer interactions,
resulting in a successful registration response.

---

## Conclusion
This technical documentation consolidates all architectural and design decisions made in Part 1 of the project.
It serves as a reference for future implementation phases and ensures consistency between design and development.
