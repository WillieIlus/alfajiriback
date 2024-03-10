from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class Plan(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price per day'))
    trial_days = models.PositiveIntegerField(default=0, verbose_name=_('Trial days'))
    max_jobs = models.PositiveIntegerField(default=0, verbose_name=_('Max jobs'))
    is_default = models.BooleanField(default=False, verbose_name=_('Is default'),
                                        help_text=_('If this plan is default, it will be assigned to new users.'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    is_fallback = models.BooleanField(default=False, verbose_name=_('Is fallback'),
                                        help_text=_('If this plan is fallback, it will be assigned to users who have no active plan.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    weight = models.PositiveIntegerField(default=0, verbose_name=_('Weight'),
                                        help_text=_('Plans with higher weight will be shown first.'))

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plans')
        ordering = ('weight', 'id')

    def __str__(self):
        return f'{self.title}: Ksh {self.price_per_day} per day'


