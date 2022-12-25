from django.db import models

from advertisement.enums import AdPriorityType


# Create your models here.

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Advertisement(AbstractBaseModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    ad_priority = models.CharField(max_length=15, null=False, blank=False, choices=AdPriorityType.choices(),
                                   default=AdPriorityType.HIGH)
    ad_status = models.CharField(max_length=15, null=False, blank=False, choices=AdPriorityType.choices(),
                                 default=AdPriorityType.HIGH)

    class Meta:
        db_table = 'advertisement'


class BQExampleData(models.Model):
    name = models.CharField(max_length=250, null=True, blank=False, default=None)
    description = models.TextField()
    phone_number = models.CharField(max_length=250, null=True, blank=False, default=None)

    class Meta:
        db_table = 'bq_example_data'
