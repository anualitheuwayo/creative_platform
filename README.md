Creative Platform Backend
Creative Platform is a RESTful backend API that connects Artists with Clients in one place. It allows Artists to create professional profiles, showcase their artwork, upload profile and artwork images, and manage how their contact information is displayed publicly. Clients can create accounts, browse Artist profiles and artwork, and interact with the platform’s available creative-service features.

The project is built with FastAPI, SQLAlchemy, and Pydantic, following a layered architecture that separates API routing, validation, business logic, database access, and database models. This structure makes the backend easier to test, maintain, and extend as new features are added.

Key Features
User registration and authentication using JWT access tokens.

Role-based access control for Artists and Clients.

Artist profile creation, retrieval, update, and deletion.

One Artist Profile per Artist account.

Artist profile details including biography, specialization, location, hourly rate, and verification status.

Profile image upload with JPEG, PNG, and WEBP validation.

Artwork creation and management for Artists.

Artwork image upload and local file storage.

Public browsing of Artist profiles and artwork.

Artist phone-number privacy controls:

Artists can save their phone number.

Artists choose whether it is publicly visible.

Private phone numbers are hidden from public endpoints.

Artists can always view and update their own phone number.

Automated tests for authentication, permissions, profile management, uploads, validation, and privacy behavior.

Architecture
The API follows a layered backend structure:

text
Client Application
        ↓
FastAPI Routers
        ↓
Pydantic Schemas
        ↓
Service Layer
        ↓
Repository Layer
        ↓
SQLAlchemy Models
        ↓
Database
Each layer has a focused responsibility:

Routers handle HTTP endpoints, request dependencies, and responses.

Schemas validate incoming data and serialize API output.

Services enforce business logic, access control, ownership rules, and privacy rules.

Repositories perform database CRUD operations.

Models define database tables and relationships.

Tests verify that API behavior remains correct as the application grows.

Technology Stack
Python

FastAPI

SQLAlchemy

Pydantic

JWT authentication

Pytest

SQLite for local development, with support for moving to PostgreSQL later

Local image storage for profile and artwork uploads

Privacy and Security
The platform includes role-based authorization and ownership checks to ensure that users can only manage their own data. Artist phone numbers are private by default and are returned in public Artist Profile endpoints only when the Artist explicitly enables visibility.

Uploaded images are validated by MIME type and file extension, assigned UUID-based filenames, and stored outside version control. The project’s .gitignore excludes environment secrets, virtual environments, Python cache files, and uploaded images.

Project Status
The backend currently includes core platform functionality for user accounts, Artist Profiles, image uploads, artwork management, access control, and phone-number privacy. The automated test suite currently passes successfully, confirming that the implemented features work together without breaking existing functionality.