# Custom authentication in django

https://docs.djangoproject.com/en/dev/topics/http/sessions/

Creating a backend:

```
class auth(object):
    def sessionStore(self):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        return SessionStore()

    def authenticate(self, username=None, password=None):
        if authuser(username, password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = User(username=username, password='get from settings.py')
                user.is_staff = True
                user.save()
            s = self.sessionStore()
            s['gitlab_private_token'] = u['private_token']
            s.save()
            return user
        return None

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
```

Add as a backend in settings.py

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    #'allauth.account.auth_backends.AuthenticationBackend',
    'kooplexhub.gitlab.auth'
)
