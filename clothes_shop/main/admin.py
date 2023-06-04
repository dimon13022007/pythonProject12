from django.contrib import admin


from .models import User

admin.site.register(User)

from .models import Article

admin.site.register(Article)

from .models import Message

admin.site.register(Message)



