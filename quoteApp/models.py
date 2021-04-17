from django.db import models
from login.models import User

# Create your models here.
class QuoteManager(models.Manager):
    def validator(self, postData, id):
        curr_user = User.objects.get(id=id)
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author name needs to be greater than 3 characters."
        if len(postData['quote']) < 10:
            errors['quote'] = "Quote needs to be greater than 10 characters"
        return errors


class Quote(models.Model):
    content = models.TextField()
    author = models.CharField(max_length=50)
    poster = models.ForeignKey(User, related_name="quoter",on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(User, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

