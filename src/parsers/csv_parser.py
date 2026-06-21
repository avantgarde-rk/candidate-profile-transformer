import csv

from src.models.candidate import RawCandidate


class CSVParser:

    @staticmethod
    def parse(file_path: str) -> RawCandidate:

        with open(
            file_path,
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            required_columns = {
                "name",
                "email",
                "phone"
            }

            if not reader.fieldnames:

                raise ValueError(
                    "CSV file is empty"
                )

            missing_columns = (
                required_columns -
                set(reader.fieldnames)
            )

            if missing_columns:

                raise ValueError(
                    "Missing CSV columns: "
                    + ", ".join(
                        sorted(missing_columns)
                    )
                )

            try:
                row = next(reader)

            except StopIteration:

                raise ValueError(
                    "CSV file is empty"
                )

        return RawCandidate(
            full_name=row.get("name"),
            emails=[
                row["email"]
            ] if row.get("email") else [],
            phones=[
                row["phone"]
            ] if row.get("phone") else [],
            current_company=row.get(
                "current_company"
            ),
            current_title=row.get(
                "title"
            ),
            source="RECRUITER_CSV"
        )