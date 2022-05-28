from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name= last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#Custom User
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    avatar = models.ImageField(default='/uploads/default.jpg',upload_to='uploads/avatar/%Y/%m')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

    def show(self):
        return f'{self.first_name} {self.last_name}'


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
# Category
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name
#
class MyModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Post(MyModelBase):
    title = models.CharField(max_length=255,null=False)
    content = models.TextField(null=False)
    image = models.ImageField(default='/uploads/default.jpg',upload_to='uploads/post/%Y/%m')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    class Meta:
        unique_together = ('title','category')
        ordering = ['-id'] # order by id giảm dần

    def __str__(self):
        return self.content

class Comment(MyModelBase):
    content = models.TextField(null=False)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content

# sourcery skip: avoid-builtin-shadow
class ActionEmoji(MyModelBase):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    LIKE, HAHA, HEART = range(3)
    ACTIONS = [
        (LIKE,'like'),
        (HAHA,'haha'),
        (HEART,'heart')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS,default=LIKE)

class Rating(MyModelBase):
    rate = models.PositiveSmallIntegerField(default=0)

class PostView(MyModelBase):
    views = models.IntegerField(default=0)
    post = models.OneToOneField(Post,on_delete=models.CASCADE)    
