import phonenumbers


class PhoneNormalizer:

    @staticmethod
    def normalize(phone: str) -> str | None:

        try:

            parsed = phonenumbers.parse(
                phone,
                "IN"
            )

            if not phonenumbers.is_valid_number(parsed):
                return None

            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )

        except Exception:
            return None