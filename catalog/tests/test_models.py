from django.test import TestCase
from catalog.models import Author

# Create your tests here.
class ModelsTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
            Run once to set up non-modified data for all class methods
        """
        Author.objects.create(first_name='Big', last_name='Bob')


    def test_first_name_label(self):
        """
            setUp: Run once for every test method to setup clean data.
        """
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')


    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'Died')


    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s %s' % (author.first_name, author.last_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')
