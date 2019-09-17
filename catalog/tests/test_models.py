from django.test import TestCase
from catalog.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setupTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')
    
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    