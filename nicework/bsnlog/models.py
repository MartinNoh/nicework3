from django.db import models
from common.models import MyUser
import datetime


class BslHistory(models.Model):
    employee = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} ({1}) : {2}".format(self.employee.realname, self.created_at, self.contents)