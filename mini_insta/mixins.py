# mini_insta/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.http import Http404


class AuthProfileMixin(LoginRequiredMixin):
    """Require login and provide a `current_profile` helper in context."""
    login_url = "login"            
    redirect_field_name = "next"    

    def get_current_profile(self):
        user = self.request.user
        qs = Profile.objects.filter(user=user).order_by("pk")
        if not qs.exists():
            raise Http404("No Profile associated with this user.")
        return qs.first()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("current_profile", self.get_current_profile())
        return ctx


class CurrentUserProfileObjectMixin(AuthProfileMixin):
    def get_object(self, queryset=None):
        return self.get_current_profile()