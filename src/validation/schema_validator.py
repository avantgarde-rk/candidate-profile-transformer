class SchemaValidator:

    REQUIRED_FIELDS = [
        "candidate_name",
        "primary_email"
    ]

    @staticmethod
    def validate(output: dict):

        errors = []

        for field in (
            SchemaValidator.REQUIRED_FIELDS
        ):

            if (
                field not in output
                or output[field] is None
            ):
                errors.append(
                    f"Missing required field: {field}"
                )

        return errors