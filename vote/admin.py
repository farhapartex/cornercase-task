from django.contrib import admin
from vote.models import Vote, VoteResult
# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "employee")


@admin.register(VoteResult)
class VoteResultAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "votes")

