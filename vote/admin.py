from django.contrib import admin
from vote.models import Vote
# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "employee")
