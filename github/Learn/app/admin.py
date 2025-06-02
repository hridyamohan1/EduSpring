from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(login)
admin.site.register(tutor)
admin.site.register(user)
admin.site.register(adcourse)
admin.site.register(courseregister)
admin.site.register(gethelp)
admin.site.register(payment)
admin.site.register(session)

