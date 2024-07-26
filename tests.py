from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from .models import DataFile

class DataAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload_file')
        self.file_list_url = reverse('file_list')

    def test_upload_file(self):
        with open('/mnt/data/Employee Sample Data.xlsx', 'rb') as fp:
            response = self.client.post(self.upload_url, {'file': fp})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DataFile.objects.count(), 1)

    def test_file_list(self):
        response = self.client.get(self.file_list_url)
        self.assertEqual(response.status_code, 200)

    def test_visualize_data(self):
        data_file = DataFile.objects.create(file='uploads/Employee Sample Data.xlsx')
        visualize_url = reverse('visualize_data', args=[data_file.id])
        response = self.client.get(visualize_url)
        self.assertEqual(response.status_code, 200)


# Create your tests here.
