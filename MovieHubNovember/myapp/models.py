from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.


class Genres(models.Model):
    genre=models.CharField(max_length=120,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.genre
class Movies(models.Model):
    name=models.CharField(max_length=250,unique=True)
    genres=models.ManyToManyField(Genres,null=True)
    year=models.CharField(max_length=200)
    options=(
        ('malayalam','malayalam'),
        ('telungu','telungu'),
        ('tamil','tamil'),
        ('english','english'),
        ('hindi','hindi')
    )
    language=models.CharField(max_length=200,choices=options,default='malayalam')
    runtime=models.FloatField()
    poster_image=models.ImageField(upload_to='images',null=True,blank=True)
    description=models.CharField(max_length=200,null=True)

    @property
    def genre_names(self):
        return self.genres.all()
    
    @property
    def reviews(self):
        return Reviews.objects.filter(movies=self)
    # return self.reviews.set.all()
    # return self.review.all()> should provide related_name(review) in review model movie attribute 

    @property
    def avg_rating(self):
        ratings=Reviews.objects.filter(movies=self).values_list("rating",flat=True)
        return sum(ratings)/len(ratings) if ratings else 0
    
    def __str__(self):
        return self.name

class Reviews(models.Model):
    movies=models.ForeignKey(Movies,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    

#data redundancy
# course 1 django
# st1,course 1
# st2,course 1
