from django.db import models
import bcrypt, re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateRegistration(self, postData):
        errors = []
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 3:
            errors.append("First name must be greater than 3 characters")
        if len(postData['last_name']) < 3:
            errors.append('Last Name must be greater than 3 characters')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Please enter a valid email address')
        if len(existing_user):
            errors.append('This email already exists')
        if len(postData['pw']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['pw'] != postData['cpw']:
            errors.append('Passwords must match')
        if len(errors):
            return errors
        me = User.objects.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password= bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            )
        return me

    def validateLogin(self, postData):
        errors = []
        existing_user_list = User.objects.filter(email=postData['email'])
        if len(existing_user_list):
            if bcrypt.checkpw(postData['pw'].encode(), existing_user_list[0].password.encode()):
                return existing_user_list[0]
        return 'invalid email / password combination'

class TripManager(models.Manager):
    def validateTrip(self, postData, user_id):
        errors = []
        if len(postData['location']) < 1:
            errors.append('Please enter a destination')
        if len(postData['desc']) < 1:
            errors.append('Please enter a description')
        print(datetime.datetime.now())
        if postData['start'] < str(datetime.datetime.now()):
            errors.append('Start date must be later than today')
        if postData['end'] < postData['start']:
            errors.append('End date must be after start date')
        if len(errors):
            return errors
        this = Trip.objects.create(
            location=postData['location'],
            start=postData['start'],
            end=postData['end'],
            desc=postData['desc'],
            created_by=User.objects.get(id=postData['user_id'])
        )
        return this

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    location = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    desc = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='planner')
    joined_by = models.ManyToManyField(User, related_name='joined')
    objects = TripManager()

# Create your models here.
