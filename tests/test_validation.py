from src.validation.schema_validator import (
    SchemaValidator
)


def test_validation():

    output = {
        "candidate_name": "Rakesh",
        "primary_email": "rakesh@gmail.com"
    }

    errors = SchemaValidator.validate(
        output
    )

    assert errors == []