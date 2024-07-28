from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from locations.models import Location
from categories.models import Category

User = settings.AUTH_USER_MODEL


class CompanyManager(models.Manager):
    def with_jobs_count(self):
        return self.annotate(total_jobs_count=Count('job'))


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    logo = models.ImageField(upload_to='companies/logos/', blank=True, null=True)
    cover = models.ImageField(upload_to='companies/', verbose_name=_('Cover'), blank=True, null=True)
    website = models.URLField(verbose_name=_('Website'), blank=True, null=True)
    phone = models.CharField(max_length=255, verbose_name=_('Phone'), blank=True, null=True)
    email = models.EmailField(verbose_name=_('Email'), blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name=_('Specific location'), blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'), related_name='companies',
                             blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='companies')
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Location'),
                                 related_name='companies')
    job_count = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    objects = CompanyManager()

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ('created_at', '-job_count', '-updated_at', 'name')

    # def __str__(self):
    #     return self.name

    def __str__(self):
        # Example handling None case for title
        return str(self.name) if self.name is not None else "Untitled Job"

    def get_absolute_url(self):
        return reverse('companies:detail', kwargs={'slug': self.slug})

    @property
    def truncated_description(self):
        max_length = 170
        if len(self.description) > max_length:
            return self.description[:max_length] + '...'
        else:
            return self.description

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)


@receiver(post_save, sender=Company)
def send_company_notification(sender, instance, created, **kwargs):
    if created and instance.email:  # Check if it's a new company and email is provided
        # Email to admin
        admin_subject = f"New Company Added: {instance.name}"
        admin_message = f"A new company has been added:\n\nName: {instance.name}\nDescription: {instance.truncated_description}\nWebsite: {instance.website}"
        admin_from_email = settings.DEFAULT_FROM_EMAIL
        admin_recipient_list = [settings.ADMIN_EMAIL]

        send_mail(admin_subject, admin_message, admin_from_email, admin_recipient_list)

        # Email to company
        company_subject = f"Welcome to Our Platform, {instance.name}!"
        html_message = render_to_string('emails/company_welcome.html', {'company': instance})
        plain_message = strip_tags(html_message)
        company_from_email = settings.DEFAULT_FROM_EMAIL
        company_recipient_list = [instance.email]

        send_mail(company_subject, plain_message, company_from_email, company_recipient_list, html_message=html_message)

def get_jobs(self):
    return self.jobs.all()


def get_logo_url(self):
    if self.logo:
        return self.logo.url
    else:
        return '/static/images/default-company-logo.png'
