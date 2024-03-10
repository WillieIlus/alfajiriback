# We are going to create a custom user model to replace the default user model and make it robust like one of facebook or twitter.
# We are going to use AbstractBaseUser and BaseUserManager to create our custom user model.
# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.conf import settings

import uuid

class CustomAccountManager(BaseUserManager):
  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError(_('The Email must be set'))
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)
  
  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    
    if extra_fields.get('is_staff') is not True:
      raise ValueError(_('Superuser must have is_staff=True.'))
    if extra_fields.get('is_superuser') is not True:
      raise ValueError(_('Superuser must have is_superuser=True.'))
    
    return self._create_user(email, password, **extra_fields)
  
class User(AbstractBaseUser, PermissionsMixin):
  GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
  )

  ROLE = (
    ('admin', 'Admin'),
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('manager', 'Manager'),
    ('employee', 'Employee'),

  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.EmailField(_('email address'), unique=True)
  first_name = models.CharField(_('first name'), max_length=150, blank=True)
  last_name = models.CharField(_('last name'), max_length=150, blank=True)
  middle_name = models.CharField(_('middle name'), max_length=150, blank=True)
  avatar = models.ImageField(_('avatar'), upload_to='avatars/', default='avatars/default')
  role = models.CharField(_('role'), max_length=20, choices=ROLE, default='user')
  gender = models.CharField(_('gender'), max_length=1, choices=GENDER, default='M')

  address = models.CharField(_('address'), max_length=255, blank=True)
  city = models.CharField(_('city'), max_length=100, blank=True)

  phone = models.CharField(_('phone'), max_length=15, blank=True)
  date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
  bio = models.TextField(_('bio'), blank=True)
  website = models.URLField(_('website'), blank=True)

  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
  is_active = models.BooleanField(_('active'), default=True)
  is_staff = models.BooleanField(_('staff status'), default=False)
  is_superuser = models.BooleanField(_('superuser status'), default=False)
  
  objects = CustomAccountManager()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'phone']
  
  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
    ordering = ['-date_joined']
  
  def email_user(self, subject, message, from_email=None, **kwargs):
    send_mail(subject, message, from_email, [self.email], **kwargs)
    
  def __str__(self):
    return self.email
  
  def get_full_name(self):
    return f'{self.first_name} {self.last_name}'
  
  def get_short_name(self):
    return self.first_name
  
  def has_perm(self, perm, obj=None):
    return self.is_superuser
  
  def get_avatar(self):
    if self.avatar:
      return self.avatar.url
    return settings.STATIC_URL + 'images/default-avatar.png'
  
