from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection


class DatabaseConnectionTest(TestCase):
    """Test database connectivity"""
    
    def test_database_connection(self):
        """Test that we can connect to the database"""
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertEqual(result[0], 1)
    
    def test_database_name(self):
        """Test that we're using the correct database"""
        db_name = connection.settings_dict['NAME']
        self.assertIsNotNone(db_name)
        self.assertGreater(len(db_name), 0)


class AdminAccessTest(TestCase):
    """Test admin panel accessibility"""
    
    def test_admin_url_exists(self):
        """Test that admin URL is configured"""
        url = reverse('admin:index')
        self.assertIsNotNone(url)
    
    def test_admin_login_page(self):
        """Test admin login page loads (redirects to login if not authenticated)"""
        response = self.client.get('/admin/')
        # Admin redirects to login page (302) if not authenticated, or 200 if logged in
        self.assertIn(response.status_code, [200, 302])


class UserModelTest(TestCase):
    """Test user model functionality"""
    
    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_count(self):
        """Test user count"""
        initial_count = User.objects.count()
        User.objects.create_user('user1', 'user1@test.com', 'pass123')
        self.assertEqual(User.objects.count(), initial_count + 1)


class SettingsTest(TestCase):
    """Test Django settings"""
    
    def test_debug_mode(self):
        """Test that DEBUG is set"""
        from django.conf import settings
        self.assertIsNotNone(settings.DEBUG)
    
    def test_database_config(self):
        """Test database configuration"""
        from django.conf import settings
        db_config = settings.DATABASES['default']
        self.assertEqual(db_config['ENGINE'], 'django.db.backends.postgresql')
        self.assertIsNotNone(db_config['NAME'])
