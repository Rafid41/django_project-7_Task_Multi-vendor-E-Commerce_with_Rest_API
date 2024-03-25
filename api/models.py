from django.db import models


# Create your models here.
# ################################# daily data ###################
class DailyData(models.Model):
    date_data = models.CharField(max_length=30)  # Date field to store the date
    revenue = models.FloatField(default=0)

    def __str__(self):
        return f"Date: {self.date_data}, Revenue: {self.revenue}"

    class Meta:
        ordering = ["-date_data"]
