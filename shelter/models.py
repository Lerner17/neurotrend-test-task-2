from django.db import models
from django.utils.translation import gettext as _
import uuid


class Breed(models.Model):

    class Meta:
        verbose_name = _('Breed')
        verbose_name_plural = _('Breeds')

    title = models.CharField(_('title'), max_length=64,
                             blank=False, unique=True, null=False)

    def __str__(self):
        return self.title


class Dog(models.Model):

    SEXS = (
        ('M', _('Male'),),
        ('F', _('Female'),),
    )

    class Meta:
        verbose_name = _('Dog')
        verbose_name_plural = _('Dogs')

    nickname = models.CharField(
        _('nickname'), max_length=64, blank=True, null=True)
    breed = models.ForeignKey(
        Breed, blank=False, null=True, on_delete=models.SET_NULL, verbose_name=_('Breed'))
    weight = models.FloatField(
        _('weight'), blank=False)
    height = models.FloatField(
        _('Growth at the withers'), blank=False)
    date_of_birth = models.DateField(_('Date of birth'), blank=True, null=True)
    guardian = models.ForeignKey(
        'Guardian', blank=True, on_delete=models.SET_NULL, null=True)
    sex = models.CharField(_('Sex'), max_length=1, choices=SEXS)
    image = models.ImageField(
        _('Photo'), upload_to='dogs_photo', blank=True, null=True)

    def __str__(self):
        return f'{self.id} | {self.get_nickname}'

    @property
    def get_nickname(self):
        if self.nickname is not None:
            return self.nickname
        else:
            return _("Name not specified")


class Guardian(models.Model):

    class Meta:
        verbose_name = _('Guardian')
        verbose_name_plural = _('Guardians')

    first_name = models.CharField(_('First name'), max_length=64, blank=False)
    middle_name = models.CharField(
        _('Middle name'), max_length=64, blank=True, null=True)
    last_name = models.CharField(_('Last name'), max_length=64, blank=False)
    phone_number = models.CharField(_('phone'), max_length=16, blank=False)
    address = models.CharField(
        _('Address'), max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.id} | {self.last_name}'

    def dogs_count(self) -> int:
        return self.dog_set.all().count()


class Payment(models.Model):
    '''Dog donation check'''

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    target = models.ForeignKey(
        Dog, on_delete=models.CASCADE, verbose_name=_('Target for donation'))
    price = models.PositiveIntegerField(blank=False)
    date_of_pay = models.DateTimeField(auto_now=True)
    is_success = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return f'Чек №{self.uuid} - {self.date_of_pay} {self.price}'
