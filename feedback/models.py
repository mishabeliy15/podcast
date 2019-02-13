from django.db import models


class Feedback(models.Model):
    owner = models.ForeignKey('auth.User', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    positive = models.TextField(null=True, blank=True)
    negative = models.TextField(null=True, blank=True)
    bugs = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.positive:
            return self.positive
        elif self.negative:
            return self.negative
        elif self.bugs:
            return self.bugs
        else:
            return self.owner.username
