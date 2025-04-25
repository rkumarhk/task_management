from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from projects.models import Project, Task, Comment

class TaskManagementTests(APITestCase):

    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_superuser(email="admin4@example.com",  password="adminpass")
        self.project_manager = User.objects.create_user(email="manager4@example.com",   first_name= "Rohit", password="managerpass", job_role="projectmanager")
        self.developer = User.objects.create_user(email="developer4@example.com", first_name= "Manan", password="devpass", job_role="developer")

        # Authenticate admin user
        self.client.login(email="admin@example.com", password="adminpass")

        # Create a test project
        self.project = Project.objects.create(name="Test Project", description="Test Description", created_by=self.admin_user)

        # Create a test task
        self.task = Task.objects.create(title="Test Task", project=self.project, created_by=self.admin_user)

        # Create a test comment
        self.comment = Comment.objects.create(content="Test Comment", task=self.task, author=self.admin_user)

    # User Endpoints
    def test_list_users(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {"email": "newuser@example.com", "password": "newpass", "job_role": "developer"}
        response = self.client.post(reverse('user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user(self):
        response = self.client.get(reverse('user-detail', args=[self.admin_user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        data = {"first_name": "Updated"}
        response = self.client.put(reverse('user-detail', args=[self.admin_user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        response = self.client.delete(reverse('user-detail', args=[self.developer.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Project Endpoints
    def test_list_projects(self):
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        data = {"name": "New Project", "description": "New Description", "created_by": self.admin_user.id}
        response = self.client.post(reverse('project-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_project(self):
        response = self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_project(self):
        data = {"name": "Updated Project"}
        response = self.client.put(reverse('project-detail', args=[self.project.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        response = self.client.delete(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Task Endpoints
    def test_list_tasks(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        data = {"title": "New Task", "project": self.project.id, "assigned_to": self.developer.id, "created_by": self.admin_user.id}
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_task(self):
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
