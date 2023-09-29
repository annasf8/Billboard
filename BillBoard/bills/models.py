from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
# from .admin import BillAdminForm


class Bill(models.Model):

    tanks = 'TK'
    hils = 'HL'
    dd = 'DD'
    merchants = 'MH'
    guild_masters = 'GM'
    quest_givers = 'QM'
    blacksmiths = 'BS'
    tanners = 'TN'
    potion_makers = 'PM'
    spell_masters = 'SM'

    CATEGORIES = [
        (tanks, 'Танки'),
        (hils, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (guild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    categories = models.CharField(max_length=2, choices=CATEGORIES, default='TK')
    text_bill = RichTextField()
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Click(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_click = models.TextField(max_length=255)
    click_bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    click = models.BooleanField(default=False)


    def __str__(self):
        return self.text_click