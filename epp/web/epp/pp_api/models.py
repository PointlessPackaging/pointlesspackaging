from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Packager:
    name = models.CharField(max_length=50)
    count = models.IntegerField()
    score = models.DecimalField(max_digits=2, decimal_places=1)

    def computer_avg(self, curr_score):
        self.count += 1
        self.curr_avg += (curr_score - self.curr_avg) / self.count

    def update_avg(self):
        return


class Post(models.Model):
    top_image = models.ImageField(upload_to=top_img_path)
    side_image = models.ImageField(upload_to=side_img_path)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PredictedPost(models.Model):
    packager = models.ForeignKey(Packager, on_delete=models.CASCADE, blank=True, null=True)
    materials = models.CharField(max_length=100, blank=True, null=True)
    outer_size = models.IntegerField(blank=True, null=True)
    inner_size = models.IntegerField(blank=True, null=True)
    item_size = models.IntegerField(blank=True, null=True)
    score = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

