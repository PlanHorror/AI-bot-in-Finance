from django.db import models

# Create your models here.
class HistoricalData(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='csv_upload/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + ' ' + self.csv_file.name
class Result(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    historical_data = models.ForeignKey(HistoricalData, on_delete=models.CASCADE)
    result = models.ImageField(upload_to='image/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.historical_data.user.username + ' ' + self.historical_data.csv_file.name