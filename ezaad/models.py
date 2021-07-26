from django.conf import settings
from django.contrib.auth.models import (BaseUserManager,AbstractUser)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from django_scim.models import AbstractSCIMGroupMixin, AbstractSCIMUserMixin
from django_scim.views import FilterMixin


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            scim_username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#class Company(models.Model):
#    name = models.CharField(
#        _('Name'),
#        max_length=100,
#    )
#

class User(AbstractSCIMUserMixin, TimeStampedModel, AbstractUser):
    #company = models.ForeignKey(
    #    'app.Company',
    #    on_delete=models.CASCADE,
    #)

    # Why override this? Can't we just use what the AbstractSCIMUser mixin
    # gives us? The USERNAME_FIELD needs to be "unique" and for flexibility, 
    # AbstractSCIMUser.scim_username is not unique by default.
    scim_username = models.CharField(
        _('SCIM Username'),
        max_length=254,
        null=True,
        blank=True,
        default=None,
        unique=True,
        help_text=_("A service provider's unique identifier for the user"),
    )

    email = models.EmailField(
        _('Email'),
    )

    first_name = models.CharField(
        _('First Name'),
        max_length=100,
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=100,
    )

    #USERNAME_FIELD = 'scim_username'

    # objects = MyUserManager()


    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name + (' ' + self.last_name[0] if self.last_name else '')


#class Group(TimeStampedModel, AbstractSCIMGroupMixin):
#    #company = models.ForeignKey(
#    #    'app.Company',
#    #    on_delete=models.CASCADE,
#    #)
#
#    members = models.ManyToManyField(
#        settings.AUTH_USER_MODEL,
#        through='GroupMembership',
#        through_fields=('group', 'user'),
#    )
#
#    @property
#    def name(self):
#        return self.scim_display_name
#
#
#class GroupMembership(models.Model):
#    user = models.ForeignKey(
#        to=settings.AUTH_USER_MODEL,
#        on_delete=models.CASCADE,
#    )
#
#    group = models.ForeignKey(
#        to='app.Group',
#        on_delete=models.CASCADE
#    )
