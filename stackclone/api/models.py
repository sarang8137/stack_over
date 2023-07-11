from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="question_image",null=True)
    date=models.DateField(auto_now_add=True)

    @property
    def question_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.CharField(max_length=500)
    upvote=models.ManyToManyField(User,related_name="user")

    @property
    def upvote_count(self):
        return self.upvote.count()
