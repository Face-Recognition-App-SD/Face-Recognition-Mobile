"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
# from address.models import AddressField


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


GENDER_CHOICES = (

    ("Male", "Male"),
    ("Female", "Female"),
    ("Transgender", "Transgender"),
    ("Non-binary/non-conforming", "Non-binary/non-conforming"),
    ("Prefer not to respond", "Prefer not to respond"),
)


TITLE_CHOICES = (

    ("Doctor", "Doctor"),
    ("Nurse", "Nurse"),
    ("Physical Therapist", "Physical Therapist"),

)

RELATIONSHIP_CHOICES = (

    ("Spouse", "Spouse"),
    ("Mother", "Mother"),
    ("Father", "Father"),
    ("Children", "Children"),
    ("Friend", "Friend"),
    ("Not Applicable", "PNot Applicable"),
)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered "
                                 + "in the format:'+999999999'. Up" +
                                 "to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17, blank=True)
    # Validators should be a list
    # phoneNumber = PhoneNumberField
    # (unique = True, null = False, blank = False)
    # date_of_birth = models.DateField(max_length=8)
    street_address = models.CharField(max_length=255)
    city_address = models.CharField(max_length=255)
    zipcode_address = models.CharField(max_length=255)
    state_address = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        default='Prefer not to respond',
        )

    role = models.CharField(
        max_length=50,
        choices=TITLE_CHOICES,
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def greet(self):
        if self.gender == "Male":
            return 'Mr. ' + self.last_name
        elif self.gender == "Female":
            return 'Ms. ' + self.last_name
        else:
            return self.last_name

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Patient(models.Model):
    """Patient object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    patient_email = models.EmailField(max_length=255, unique=False)
    patient_first_name = models.CharField(max_length=255)
    patient_last_name = models.CharField(max_length=255)
    patient_description = models.TextField(blank=True)
    patient_med_list = models.TextField(blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered "
                                 + "in the format:'+999999999'. Up" +
                                 "to 15 digits allowed.")
    patient_phone_number = models.CharField(validators=[phone_regex],
                                            max_length=17, blank=True)
    # Validators should be a list
    # patient_phoneNumber = PhoneNumberField
    # (unique=True, null=False, blank=False)
    patient_date_of_birth = models.DateField(auto_now=False, null=True)
    patient_street_address = models.CharField(max_length=255)
    patient_city_address = models.CharField(max_length=255)
    patient_zipcode_address = models.CharField(max_length=255)
    patient_state_address = models.CharField(max_length=255)
    patient_creation_date = models.DateTimeField(auto_now_add=True)
    patient_modified_date = models.DateTimeField(auto_now=True)
    patient_link = models.CharField(max_length=255, blank=True)

    patient_gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        default='Prefer not to respond',
        )

    emergency_contact_email = models.EmailField(max_length=255, unique=False)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_phone_number = models.CharField(validators=[phone_regex],
                                              max_length=17, blank=True)

    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES,
        default='Not Applicable',
        )

    is_active = models.BooleanField(default=True)

    def greet(self):
        if self.patient_gender == "Male":
            return 'Mr. ' + self.patient_last_name
        elif self.patient_gender == "Female":
            return 'Ms. ' + self.patient_last_name
        else:
            return self.patient_last_name

    def __str__(self):
        return self.patient_first_name
