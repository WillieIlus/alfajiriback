import datetime
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone

import random, string
from datetime import datetime, timedelta, timezone, date
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.utils.timesince import timesince
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from locations.models import Location
from categories.models import Category
from companies.models import Company
from plans.models import Plan

random_string = ''.join(random.choices(string.digits, k=6))
import logging
from django.utils.text import slugify
from django.utils import timezone

logger = logging.getLogger(__name__)


class Job(models.Model):
    # Job Type
    FULL_TIME = 'Full Time'
    PART_TIME = 'Part Time'
    CONTRACT = 'Contract'
    INTERNSHIP = 'Internship'
    TEMPORARY = 'Temporary'
    FREELANCE = 'Freelance'

    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (CONTRACT, 'Contract'),
        (INTERNSHIP, 'Internship'),
        (TEMPORARY, 'Temporary'),
        (FREELANCE, 'Freelance'),
    ]
    # Currency
    KSH = 'KSH'
    USD = 'USD'
    UGH = 'UGH'
    TSH = 'TSH'
    EUR = 'EUR'
    GBP = 'GBP'
    CURRENCY_CHOICES = [
        (KSH, 'Kenya Shilling'),
        (USD, 'US Dollar'),
        (UGH, 'Uganda Shilling'),
        (TSH, 'Tanzania Shilling'),
        (EUR, 'Euro'),
        (GBP, 'British Pound'),
    ]

    PER_HOUR = 'PH'
    PER_DAY = 'PD'
    PER_WEEK = 'PW'
    PER_MONTH = 'PM'
    PER_YEAR = 'PY'
    SALARY_TYPE_CHOICES = [
        (PER_HOUR, 'Per Hour'),
        (PER_DAY, 'Per Day'),
        (PER_WEEK, 'Per Week'),
        (PER_MONTH, 'Per Month'),
        (PER_YEAR, 'Per Year'),
    ]

    PER_DAY = 'PD'
    PER_WEEK = 'PW'
    PER_MONTH = 'PM'
    PER_YEAR = 'PY'

    WORK_HOUR_CHOICES = [
        (PER_DAY, 'Per Day'),
        (PER_WEEK, 'Per Week'),
        (PER_MONTH, 'Per Month'),
        (PER_YEAR, 'Per Year'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'), blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name=_('Specific location'), blank=True, null=True)
    location = models.ForeignKey(Location, default=1, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, default=1, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, default=1, blank=True, null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='jobs/images/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)

    duration_days = models.PositiveIntegerField(default=30, validators=[MinValueValidator(1), MaxValueValidator(365)],
                                                blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default=FULL_TIME, blank=True, null=True)
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_type = models.CharField(max_length=2, choices=SALARY_TYPE_CHOICES, default=PER_MONTH, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=KSH, blank=True, null=True)

    work_experience = models.IntegerField(blank=True, null=True)
    work_hours = models.IntegerField(blank=True, null=True)
    work_hour_type = models.CharField(max_length=3, choices=WORK_HOUR_CHOICES, default=PER_DAY, blank=True, null=True)
    education_level = models.CharField(max_length=200, blank=True, null=True)
    applicants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='job_applicants', blank=True)
    
    view_count = models.IntegerField(default=0, blank=True, null=True)
    click_count = models.IntegerField(default=0, blank=True, null=True)
    apply_count = models.IntegerField(default=0, blank=True, null=True)
    bookmarks = models.IntegerField(default=0, blank=True, null=True)

    vacancies = models.IntegerField(default=1, blank=True, null=True)

    is_published = models.BooleanField(default=False, blank=True, null=True)
    is_featured = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(blank=True, null=True)

    last_viewed_at = models.DateTimeField(null=True, blank=True)
    last_clicked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Jobs"
        ordering = ['-created_at']

    def get_job_type_display(self):
        return dict(self.JOB_TYPE_CHOICES)[self.job_type]

    def __str__(self):
        return self.title + ' - ' + str(self.id)

    @property
    def truncated_description(self):
        max_length = 170
        if len(self.description) > max_length:
            return self.description[:max_length] + '...'
        else:
            return self.description

    def update_last_viewed(self):
        self.last_viewed_at = timezone.now()
        self.save()

    def update_last_clicked(self):
        self.last_clicked_at = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('jobs:detail', kwargs={'slug': self.slug})

    def get_apply_url(self):
        return reverse('jobs:apply', kwargs={'slug': self.slug})

    def get_applicants_url(self):
        return reverse('jobs:applicants', kwargs={'slug': self.slug})

    def get_applicants_count(self):
        return self.applicants.count()

    def get_applicants_list(self):
        return self.applicants.all()

    def timesince(self):
        return timesince(self.created_at, timezone.now())

    def get_location(self):
        return self.location.name

    def get_category(self):
        return self.category.name
    
    def get_company(self):
        return self.company.name

    def get_job_type(self):
        return self.get_job_type_display()

    def days_left(self):
        if self.deadline:
            today = timezone.now().date()
            days_left = (self.deadline.date() - today).days
            return max(days_left, 0)
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            title_str = str(self.title)
            company_id = str(self.company.id)
            self.slug = slugify(title_str + ' ' + company_id)
        super(Job, self).save(*args, **kwargs)



class Bookmark(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Bookmarks"
        ordering = ['-created_at']

    def __str__(self):
        return self.job.title + ' - ' + self.job.id

    def save(self, *args, **kwargs):
        super(Bookmark, self).save(*args, **kwargs)



class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    employer_email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    resume = models.FileField(upload_to='jobs/resumes/', blank=True, null=True)
    cover_letter = models.TextField(max_length=2000, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Job Applications"
        ordering = ['-created_at']

    def __str__(self):
        return self.job.title + ' - ' + self.job.id

    def get_resume_url(self):
        return reverse('jobs:resume', kwargs={'pk': self.pk})

    def get_cover_letter_url(self):
        return reverse('jobs:cover_letter', kwargs={'pk': self.pk})

    def get_resume_name(self):
        return self.resume.name.split('/')[-1]

    def get_cover_letter_name(self):
        return self.cover_letter.name.split('/')[-1]

    def save(self, *args, **kwargs):
        super(JobApplication, self).save(*args, **kwargs)


class Impression(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    source_ip = models.GenericIPAddressField(blank=True, null=True)
    session_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Impressions"
        ordering = ['-created_at']
        index_together = ('job', 'session_id',)

    def __str__(self):
        return self.job.title + ' - ' + self.source_ip

    def get_impressions_count(self):
        return Click.objects.filter(job=self.job).count()

    def get_impressions(self):
        return Click.objects.filter(job=self.job)

    def save(self, *args, **kwargs):
        super(Impression, self).save(*args, **kwargs)


class Click(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    source_ip = models.GenericIPAddressField(blank=True, null=True)
    session_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Clicks"
        ordering = ['-created_at']
        index_together = ('job', 'session_id',)

    def __str__(self):
        return self.job.title + ' - ' + self.source_ip

    def get_clicks_count(self):
        return Click.objects.filter(job=self.job).count()

    def get_clicks(self):
        return Click.objects.filter(job=self.job)

    def save(self, *args, **kwargs):
        super(Click, self).save(*args, **kwargs)


        
@receiver(post_save, sender=Bookmark)
def update_bookmark_count(sender, instance, **kwargs):
    if created:
        instance.job.bookmarks += 1
        instance.job.save()
    else:
        instance.job.bookmarks -= 1
        instance.job.save()

@receiver(post_save, sender=JobApplication)
def update_apply_count(sender, instance, **kwargs):
    if created:
        instance.job.apply_count += 1
        instance.job.save()
    else:
        instance.job.apply_count -= 1
        instance.job.save()

@receiver(post_save, sender=Impression)
def update_impression_count(sender, instance, **kwargs):
    instance.job.view_count += 1
    instance.job.save()

@receiver(post_save, sender=Click)
def update_click_count(sender, instance, **kwargs):
    instance.job.click_count += 1
    instance.job.save()

