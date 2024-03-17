from django import forms
import json

class JSONFileForm(forms.Form):
    file = forms.FileField(label='Upload CSV an Excel File', required=False)
    json_data = forms.CharField(label='Enter JSON Data', widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        json_data = cleaned_data.get('json_data')

        if not file:
            
            raise forms.ValidationError("Please upload a valid file.")
        
        #check if csv or excel file is ok
        if file:
            file_name = file.name
            if not file_name.endswith('.csv') and not file_name.endswith('.xlsx'):
                raise forms.ValidationError("Please upload a valid CSV or Excel file.")
        

        if json_data:
            try:
                # Try to load JSON data to validate its format
                json.loads(json_data)
            except json.JSONDecodeError:
                raise forms.ValidationError("Please enter valid JSON data.")

        return cleaned_data


class FileForm(forms.Form):
    file = forms.FileField(label='Upload CSV or an Excel File', required=False)

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        
        if not file:
            
            raise forms.ValidationError("Please upload a valid file.")
        
        if file:
            file_name = file.name
            if not file_name.endswith('.csv') and not file_name.endswith('.xlsx'):
                raise forms.ValidationError("Please upload a valid CSV or Excel file.")

        return cleaned_data
