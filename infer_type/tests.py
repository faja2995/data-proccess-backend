# myapp/tests.py

from io import BytesIO
from unittest.mock import MagicMock
from django.test import Client, RequestFactory, SimpleTestCase, TestCase

from infer_type.services import change_types
from infer_type.views import upload_csv
from .forms import JSONFileForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
import json
import pandas as pd


class JSONFileFormTest(TestCase):
    def test_valid_form_with_file(self):
    # Create a CSV file
        data = {'Column1': [42]}
        df = pd.DataFrame(data)

        # Save DataFrame to CSV in buffer
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        # Provide the file in form data
        form_data = {'file': buffer}
        form = JSONFileForm(data=form_data)
        
        # Ensure the form is valid
        self.assertTrue(form.is_valid())

    def test_valid_form_with_json_data(self):
        json_data = '{"key": "value"}'
        form_data = {'json_data': json_data}
        form = JSONFileForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_invalid_form_with_invalid_json_data(self):
        invalid_json_data = '{invalid json}'
        form_data = {'json_data': invalid_json_data}
        form = JSONFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        
class TestUrls(SimpleTestCase):

    def test_upload_csv_url_resolves(self):
        url = reverse('upload_csv')
        self.assertEqual(resolve(url).func, upload_csv)

    def test_change_types_url_resolves(self):
        url = reverse('change-types')
        self.assertEqual(resolve(url).func, change_types)

class UploadCSVViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_csv_url = reverse('upload_csv')

    def test_upload_csv_with_valid_data(self):
        data = {'Column1': [42]}
        df = pd.DataFrame(data)

        # Save DataFrame to CSV in buffer
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        # Create a CSV file in memory
        csv_file = buffer
        csv_file.name = 'test.csv'
        csv_file = SimpleUploadedFile("test.csv", buffer.getvalue(), content_type="text/csv")

        # Send a POST request to the view
        response = self.client.post(self.upload_csv_url, {'file': csv_file})

        # Check if the response is successful and the content type is CSV
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

        # You may want to check other aspects of the response, such as the content itself
