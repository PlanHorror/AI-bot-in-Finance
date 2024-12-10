from django import forms
from .models import HistoricalData
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = HistoricalData
        fields = ['csv_file']
# Compare this snippet from web/finance/templates/src/index.html:
class UploadTwoFilesForm(forms.Form):
    price_csv = forms.FileField(label="Price Data CSV")
    fng_csv = forms.FileField(label="Fear and Greed Index CSV")