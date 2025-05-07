from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import BankAccount
from decimal import Decimal


class AccountVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            "kyc_submitted",
            "kyc_verified",
            "verified_date",
            "verification_notes",
            "fully_activated",
            "account_status",
        ]
        read_only_fields = ["fully_activated"]

    def validate(self, data):
        kyc_verified = data.get("kyc_verified")
        kyc_submitted = data.get("kyc_submitted")
        verified_date = data.get("verified_date")
        verification_notes = data.get("verification_notes")

        if kyc_verified:
            if not verified_date:
                raise serializers.ValidationError(
                    _("Verification date is required when verifying an account.")
                )
            if not verification_notes:
                raise serializers.ValidationError(
                    _("Verification notes are required when verifying an account.")
                )

            if kyc_submitted and not all(
                [verified_date, verification_notes, kyc_verified]
            ):
                raise serializers.ValidationError(
                    _(
                        "All verification fields (KYC Verified, verification date and notes) "
                        "must be provided when KYC is submitted"
                    )
                )

        return data


class DepositSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=Decimal("0.1")
    )

    class Meta:
        model = BankAccount
        fields = ["account_number", "amount"]

    def validate_account_number(self, value):
        try:
            account = BankAccount.objects.get(account_number=value)
            self.context["account"] = account
        except BankAccount.DoesNotExists:
            raise serializers.ValidationError(_("Invalid account number."))

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["amount"] = str(representation["amount"])
        return representation


class CustomerInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name")
    email = serializers.EmailField(source="user.email")
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = [
            "account_number",
            "fullname",
            "email",
            "photo_url",
            "account_balance",
            "account_type",
            "currency",
        ]

    def get_photo_url(self, obj):
        if hasattr(obj.user, "profile") and obj.user.profile.photo_url:
            return obj.user.profile.photo_url
        return None
