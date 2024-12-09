from django import forms
from .models import HistoricalData
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = HistoricalData
        fields = ['csv_file']
# Compare this snippet from web/finance/templates/src/index.html:
