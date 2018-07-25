from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.search_util import *
import datetime, json


class ContactInfo(models.Model):
    country = models.CharField(max_length=32, null=True)
    province = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)
    postal_code = models.CharField(max_length=32, null=True)
    address = models.CharField(max_length=512, null=True)
    phone_number = models.CharField(max_length=32, null=True)


class User(AbstractUser):
    contactinfo = models.OneToOneField(ContactInfo, on_delete=models.DO_NOTHING, default='')
    is_benefactor = models.BooleanField(default=False)
    is_charity = models.BooleanField(default=False)


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')

    first_name = models.CharField(max_length=64, default='')
    last_name = models.CharField(max_length=128, default='')
    gender = models.CharField(max_length=32, default='')

    score = models.FloatField(default=-1)

    def search_filter(self, min_date_overlap, min_required_hours, min_time_overlap, schedule):
        return has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule,
                                    dateinterval_set=self.dateinterval_set)

    def has_ability(self, ability_type_ids, ability_min_score, ability_max_score):
        for ability in self.ability_set.all():
            if ability.ability_type.id in ability_type_ids and ability_min_score < ability.score < ability_max_score:
                return True
        return False


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')

    name = models.CharField(max_length=256, default='')
    score = models.FloatField(default=-1)
    benefactor_history = models.ManyToManyField(Benefactor, primary_key=False)


class Notification(models.Model):
    type = models.CharField(max_length=128, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=2048, null=True)


# for scoring abilities the type will be like Benefactor-AbilityName
# there must be one benefactor and one charity we will find out who is sender or receiver from the type field
class ScoreRequest(models.Model):
    type = models.CharField(max_length=128, default='')
    state = models.CharField(max_length=16, default='On-Hold')
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    score = models.IntegerField(default=-1)
    description = models.CharField(max_length=2048, null=True)


class AbilityRequest(models.Model):
    type = models.CharField(max_length=64, default='')
    name = models.CharField(max_length=64, default='')
    description = models.CharField(max_length=2048, null=True)


# The project field is one to one so I put it in the NonFinancialProject class
class CooperationRequest(models.Model):
    type = models.CharField(max_length=64, default='')
    state = models.CharField(max_length=16, default='On-Hold')
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=2048, null=True)
