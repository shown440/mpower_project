from django.db import models

# Create your models here.


class HOUSEHOLDModel(models.Model):
    hh_head            = models.CharField(max_length=100, blank=True, null=True)
    hh_gender          = models.CharField(max_length=100, blank=True, null=True)
    hh_age             = models.IntegerField(blank=True, null=True)
    hh_dob             = models.DateTimeField(blank=True, null=True)
    no_of_members      = models.IntegerField(blank=True, null=True)
    has_disability     = models.BooleanField(default=False) 

    class Meta:
        managed = True #False
        db_table = "HOUSEHOLD"
        
        verbose_name = 'House-Hold'
        verbose_name_plural = 'House-Holds'