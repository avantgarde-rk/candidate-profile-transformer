import json

from src.models.candidate import RawCandidate
from src.models.candidate import (
    RawCandidate,
    Location
)
from src.normalizers.country_normalizer import (
    CountryNormalizer
)

class ATSParser:
    @staticmethod
    def parse(file_path: str) -> RawCandidate:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            location = None
            if data.get("location"):

                location_data = data["location"]

                location = Location(
                    city=location_data.get("city"),
                    region=location_data.get("region"),
                    country=CountryNormalizer.normalize(
                        location_data.get("country")
                    )
                )

        return RawCandidate(
            full_name=data.get("candidateName"),
            emails=[data["candidateEmail"]]
            if data.get("candidateEmail")
            else [],
            phones=[data["candidatePhone"]]
            if data.get("candidatePhone")
            else [],
            skills=data.get("skills", []),
            location=location,
            current_company=data.get("currentCompany"),
            current_title=data.get("jobTitle"),
            source="ATS_JSON"
        )