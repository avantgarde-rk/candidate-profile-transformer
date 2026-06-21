import json

from src.parsers.ats_parser import ATSParser
from src.parsers.resume_parser import ResumeParser
from src.parsers.csv_parser import CSVParser

from src.merger.merge_engine import MergeEngine

from src.projection.projection_engine import (
    ProjectionEngine
)

from src.validation.schema_validator import (
    SchemaValidator
)


class CandidatePipeline:

    @staticmethod
    def run(
        ats_path,
        resume_path,
        csv_path,
        config_path
    ):

        try:

            ats_candidate = ATSParser.parse(
                ats_path
            )

        except FileNotFoundError:

            raise FileNotFoundError(
                f"ATS file not found: {ats_path}"
            )

        except json.JSONDecodeError:

            raise ValueError(
                "Invalid ATS JSON format"
            )

        try:

            resume_candidate = ResumeParser.parse(
                resume_path
            )

        except FileNotFoundError:

            raise FileNotFoundError(
                f"Resume file not found: {resume_path}"
            )

        except Exception as e:

            raise ValueError(
                f"Resume parsing failed: {str(e)}"
            )

        try:

            csv_candidate = CSVParser.parse(
                csv_path
            )

        except FileNotFoundError:

            raise FileNotFoundError(
                f"CSV file not found: {csv_path}"
            )

        except Exception as e:

            raise ValueError(
                f"CSV parsing failed: {str(e)}"
            )

        merged_profile = MergeEngine.merge(
            [
                ats_candidate,
                resume_candidate,
                csv_candidate
            ]
        )

        try:

            with open(
                config_path,
                "r",
                encoding="utf-8"
            ) as f:

                config = json.load(f)

        except FileNotFoundError:

            raise FileNotFoundError(
                f"Config file not found: {config_path}"
            )

        except json.JSONDecodeError:

            raise ValueError(
                "Invalid config JSON format"
            )

        projected_output = (
            ProjectionEngine.project(
                merged_profile,
                config
            )
        )

        validation_errors = (
            SchemaValidator.validate(
                projected_output
            )
        )

        return (
            projected_output,
            validation_errors
        )