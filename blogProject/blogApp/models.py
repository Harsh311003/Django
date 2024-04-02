
# from django.contrib.auth import get_user_model

# models.py
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg

class CustomUser(AbstractUser):
    email = models.EmailField(unique = True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    # Add any additional fields you need for your user model
    def is_admin_user(self):
        return self.is_staff and self.is_superuser


# User = get_user_model()





class Category(models.Model):
    name = models.CharField( max_length = 255, unique = True)



class Blog(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField( )
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE, db_index = True)
    created_time = models.DateTimeField(auto_now_add = True)
    categories = models.ManyToManyField(Category)
    status = models.BooleanField(default = False, db_index = True)
    image_field = models.ImageField(upload_to='images/', default='images/default-blog-thumb.png')

    def count_likes(self):
        return Like.objects.filter( blog=self).count()
    
    def find_avg_rating(self):        
        ratings = self.ratings.all()  
        avg_rating = ratings.aggregate(Avg('value'))['value__avg']
        return avg_rating if avg_rating is not None else 0


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.user.username} liked {self.post}"

class Rating(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=2, decimal_places=1)  # Assuming the rating is an integer value (e.g., 1 to 5)

    # class Meta:
    #     unique_together = ('book', 'user')
