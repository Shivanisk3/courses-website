from django.contrib import admin
from .models import Section, register_table, add_course, cart, Order, Content

# Register your models here.

class SectionAdmin(admin.ModelAdmin):
	list_display = ["id","sec_name","description", "added_on"]

#admin.site.register(Reg)
admin.site.register(Section,SectionAdmin)
admin.site.register(register_table)
admin.site.register(add_course)
admin.site.register(cart)
admin.site.register(Order)
admin.site.register(Content)