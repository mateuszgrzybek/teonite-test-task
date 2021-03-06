from django.db import models


class Authors(models.Model):
    author_id = models.CharField(primary_key=True, max_length=50)
    author_name = models.CharField(max_length=50)

    class Meta:
        ordering = ('author_id',)
        db_table = 'authors'


class WordsPerAuthor(models.Model):
    author_id = models.CharField(max_length=50)
    word = models.CharField(max_length=50)
    word_count = models.IntegerField()

    class Meta:
        ordering = ('-word_count',)
        db_table = 'personal_words'


class TotalWords(models.Model):
    word = models.CharField(max_length=50)
    word_count = models.IntegerField()

    class Meta:
        ordering = ('-word_count',)
        db_table = 'total_words'
