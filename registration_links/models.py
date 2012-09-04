from django.db import models
from registration import signals
import string
import random
from . import SimpleBackend
from django.dispatch import receiver
from django.db.models import F


def id_generator(size=3, chars=string.ascii_lowercase + string.digits):
    """Generate a simple random id consiting of lowercase letters and digits"""
    return ''.join(random.choice(chars) for x in range(size))


class RegistrationLink(models.Model):
    # Just a label for easier indetification
    recipient = models.CharField(max_length=100, blank=True)
    # Custom link code
    code = models.CharField(max_length=8, blank=True, default=None)
    # How many times the link has been used for successful registration
    used_times = models.IntegerField(null=True, default=0)
    # How many times it can be used
    use_threshold = models.IntegerField(null=True, default=50)
    # Indicate if link is still active
    active = models.BooleanField(default=True, editable=True)

    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs):
        # If no custom link code, generate one
        if not self.code:
            self.code = id_generator()
        # Call the "real" save() method
        super(RegistrationLink, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.recipient + " Code:" + self.code + " " + str(self.used_times) + "/" + str(self.use_threshold)


@receiver(signals.user_registered, sender=SimpleBackend)
def user_registered_callback(sender, **kwargs):
    """When user completes registration increment the counter of used_times and remove session variable"""
    req_link_id = int(kwargs['request'].session["reg_link"])
    reg_link = RegistrationLink.objects.get(id=req_link_id)
    reg_link.used_times = F('used_times') + 1
    reg_link.save()

    # Update session
    del kwargs['request'].session["reg_link"]
