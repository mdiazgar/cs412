from django.db import models

# Create your models here.
class Article(models.Model):
    "Encapsulate the data of a mini insta"
    
    #define the data attributes of the Article object
    title=models.TextField(blank=True)
    author=models.TextField(blank=True)
    text=models.TextField(blank=True)
    published= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        "return a string representation of this model instance"
        return f'{self.title} by {self.author}' 