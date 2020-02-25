from django.contrib import admin
from .models import Dog, Guardian, Breed, Payment
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


@admin.register(Dog)
class DogModelAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('nickname',)},),
        (_('Biometric info'), {'fields': (
            'breed',
            'height',
            'weight',
            'sex',
            'date_of_birth',
        )}),
        (_('Appearance'), {'fields': ('image',)},),
        (_('Guardianship'), {'fields': ('guardian',)}),
    )

    search_fields = ('id', 'nickname')

    list_display = ('id', 'get_image', 'get_nickname',
                    'breed', 'sex', 'height', 'weight', 'date_of_birth', 'is_have_guardian', 'get_dogs_money',)

    list_display_links = ('id', 'get_image', 'get_nickname',)
    list_filter = ('breed', 'sex',)

    def is_have_guardian(self, obj) -> bool:
        if obj.guardian is not None:
            return True
        return False
    is_have_guardian.boolean = True
    is_have_guardian.short_description = _('Has the guardian?')

    def get_nickname(self, obj):
        return obj.get_nickname
    get_nickname.short_description = _('Nickname')

    def get_dogs_money(self, obj) -> str:
        return str(sum([pay.price for pay in obj.payment_set.all()])) + '₽'
    get_dogs_money.short_description = (_('Dogs money'))

    def get_image(self, obj) -> str:
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" height="80" />')
        return mark_safe('<img src="https://via.placeholder.com/150x80" height="80" />')

    get_image.short_description = _('photo')


class DogInline(admin.TabularInline):

    model = Dog


@admin.register(Guardian)
class GuardianModelAdmin(admin.ModelAdmin):

    fieldsets = (
        (_('Info'), {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'phone_number',
                'address'
            )
        }),
    )

    list_display = ('id', 'get_name', 'phone_number',
                    'get_address', 'dogs_count',)
    list_display_links = ('id', 'get_name')
    search_fields = ('id', 'phone', 'get_name',)

    inlines = (DogInline,)

    def get_name(self, obj):
        if obj.middle_name is None:
            return f'{obj.first_name[:1]}. {obj.last_name}'
        return f'{obj.first_name[:1]}. {obj.middle_name}. {obj.last_name}'
    get_name.short_description = _('Full name')

    def get_address(self, obj) -> bool:
        return obj.address is not None
    get_address.boolean = True
    get_address.short_description = _('Is the address specified?')


admin.site.register(Breed)
admin.site.register(Payment)
