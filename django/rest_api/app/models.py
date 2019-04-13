from django.db import models

class Authors(models.Model):
    author_id = models.CharField(primary_key=True, maxlength=50)
    author_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('author_id')
        db_table = 'authors'
