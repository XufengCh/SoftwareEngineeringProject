from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import EmailField


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "nickname")
        field_classes = {
            'username': EmailField,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
