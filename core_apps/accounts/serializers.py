from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import BankAccount


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
