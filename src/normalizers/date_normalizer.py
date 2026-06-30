from datetime import datetime


class DateNormalizer:

    DATE_FORMATS = [
        "%Y-%m",
        "%Y/%m",
        "%B %Y",
        "%b %Y"
    ]

    @staticmethod
    def normalize(date_value: str | None) -> str | None:

        if not date_value:
            return None

        cleaned = date_value.strip()

        for date_format in DateNormalizer.DATE_FORMATS:

            try:

                parsed_date = datetime.strptime(
                    cleaned,
                    date_format
                )

                return parsed_date.strftime(
                    "%Y-%m"
                )

            except ValueError:
                continue

        return None