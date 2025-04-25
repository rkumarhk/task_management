# 📝 Task Management System

A **Django-based Task Management System** designed to streamline project management by enabling users to manage projects, tasks, and comments efficiently. This system supports **user authentication**, **role-based access control**, **filtering**, **pagination**, and **caching**.

---

## 🚀 Features

### 🔐 **User Management**
- User registration and login with **JWT authentication**.
- Role-based access control: `superadmin`, `admin`, `projectmanager`, `developer`, `client`.
- Account activation and status management.

### 📂 **Project Management**
- Create, update, delete, and retrieve projects.
- Filter projects by `status`, `priority`, and `created_by`.
- Pagination for project lists.

### ✅ **Task Management**
- Create, update, delete, and retrieve tasks.
- Assign tasks to users.
- Filter tasks by `status` and `priority`.
- Pagination for task lists.

### 💬 **Comment Management**
- Add comments to tasks.
- Reply to comments (nested comments).
- Soft delete comments.
- Filter comments by `content`, `author`, and `task`.

### ⚡ **Performance Enhancements**
- **Caching**: Redis-based caching for frequently accessed data.
- **Pagination**: Efficient handling of large datasets.

### 📄 **API Documentation**
- Interactive API documentation using **Swagger** (`drf-yasg`).

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL
- Redis (for caching)

### Steps to Set Up the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/task-management.git
   cd task-management
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**:
   Update the `DATABASES` section in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'task',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**:
   - Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - Swagger API Docs: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## 📚 API Endpoints

### **User Endpoints**
- **POST** `/api/users/register/` - Register a new user.
- **POST** `/api/users/login/` - Login and get JWT tokens.
- **GET** `/api/users/` - List all users (admin only).
- **GET** `/api/users/<id>/` - Retrieve a specific user.

### **Project Endpoints**
- **GET** `/api/projects/` - List all projects (with filters and pagination).
- **GET** `/api/projects/<id>/` - Retrieve a specific project.
- **POST** `/api/projects/` - Create a new project.
- **PUT** `/api/projects/<id>/` - Update a project.
- **DELETE** `/api/projects/<id>/` - Delete a project.

### **Task Endpoints**
- **GET** `/api/tasks/` - List all tasks (with filters and pagination).
- **GET** `/api/tasks/<id>/` - Retrieve a specific task.
- **POST** `/api/tasks/` - Create a new task.
- **PUT** `/api/tasks/<id>/` - Update a task.
- **DELETE** `/api/tasks/<id>/` - Delete a task.

### **Comment Endpoints**
- **GET** `/api/comments/` - List all comments (with filters and pagination).
- **GET** `/api/comments/<id>/` - Retrieve a specific comment.
- **POST** `/api/comments/` - Add a new comment.
- **PUT** `/api/comments/<id>/` - Update a comment.
- **DELETE** `/api/comments/<id>/` - Delete a comment.

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@localhost:5432/task_management
REDIS_URL=redis://127.0.0.1:6379/1
```

---

## 🛠️ Technologies Used

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: PostgreSQL
- **Caching**: Redis
- **API Documentation**: drf-yasg (Swagger)

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---



### 🎉 Happy Coding!