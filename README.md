# Social Media API with FastAPI

A robust API project built with FastAPI and Python for managing social media posts, comments, user registration, authentication, and more. It leverages async database handling, background tasks, external services (like Mailgun and Backblaze B2), and advanced configurations using Pydantic.

## ✨ Features

### Post and Comment Management

📝 Create and read posts  
💬 Add comments to posts  
👍 Like posts  

### User Management

🔐 User registration with email confirmation  
🔑 Password hashing and authentication via JWT
🔗 OAuth (optional)  
👤 Manage user profiles with relational data  
🔒 Secure user routes using access tokens  

### Database Integration

🗄️ Async database setup with PostgreSQL  
🛠️ SQLAlchemy ORM for queries  
⚙️ Environment-based configurations with Pydantic  
🗃️ Caching configurations  

### Background Tasks & File Uploads

⏳ Background task processing (e.g., email notifications, image generation)  
📁 File upload management (with integration to Backblaze B2)  
🖼️ Image generation using DeepAI  

### Testing

✅ Comprehensive test coverage for posts, comments, user registration, and file uploads using pytest  

## 🛠️ Technologies Used

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM for PostgreSQL
- **Pydantic** - Data validation and settings management
- **PostgreSQL** - Database
- **Passlib** - Password hashing
- **Mailgun** - Sending emails
- **Backblaze B2** - File storage
- **DeepAI** - Image generation
- **pytest** - Testing framework
