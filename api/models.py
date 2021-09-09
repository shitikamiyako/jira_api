from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid

User = get_user_model()


def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.user_profile.id) + str(".") + str(ext)])


class Profile(models.Model):
    user_profile = models.OneToOneField(
        User, related_name='user_profile',
        on_delete=models.CASCADE
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.user_profile.username


class Category(models.Model):
    item = models.CharField(max_length=100)

    def __str__(self):
        return self.item


class Task(models.Model):
    # フォーム側で以下の選択肢から値を選択させる
    STATUS = (
        ('1', 'Not Yet'),
        ('2', 'On Going'),
        ('3', 'Done')
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    criteria = models.CharField(max_length=100)
    # 上記のSTATUSからいずれかを選択
    status = models.CharField(max_length=100, choices=STATUS, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # MinValueValidatorを使ってマイナスを許容しないようにする
    estimate = models.IntegerField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task
