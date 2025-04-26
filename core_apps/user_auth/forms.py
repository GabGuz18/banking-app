from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = [
            "email",
            "id_no",
            "first_name",
            "middle_name",
            "last_name",
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Email already exists."))
        return email

    def clean_id_no(self):
        id_no = self.cleaned_data.get("id_no")
        if User.objects.filter(id_no=id_no).exists():
            raise ValidationError(_("ID number already exists."))
        return id_no

    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get("is_superuser")
        security_question = cleaned_data.get("security_question")
        security_answer = cleaned_data.get("security_answer")

        if not is_superuser:
            if not security_question:
                self.add_error("security_question", _("Security question is required."))
            if not security_answer:
                self.add_error("security_answer", _("Security answer is required."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = [
            "email",
            "id_no",
            "first_name",
            "middle_name",
            "last_name",
            "security_question",
            "security_answer",
            "is_staff",
            "is_superuser",
            "is_active",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_("Email already exists."))
        return email

    def clean_id_no(self):
        id_no = self.cleaned_data.get("id_no")
        if User.objects.exclude(pk=self.instance.pk).filter(id_no=id_no).exists():
            raise ValidationError(_("ID number already exists."))
        return id_no

    def clean(self):
        cleaned_data = super().clean()
        is_superuser = cleaned_data.get("is_superuser")
        security_question = cleaned_data.get("security_question")
        security_answer = cleaned_data.get("security_answer")

        if not is_superuser:
            if not security_question:
                self.add_error("security_question", _("Security question is required."))
            if not security_answer:
                self.add_error("security_answer", _("Security answer is required."))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
