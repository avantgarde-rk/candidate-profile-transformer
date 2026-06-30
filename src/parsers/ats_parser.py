import json

from src.models.candidate import RawCandidate
from src.models.candidate import (
    RawCandidate,
    Location
)
from src.normalizers.country_normalizer import (
    CountryNormalizer
)
from src.models.candidate import (
    RawCandidate,
    Location,
    Experience
)
from src.normalizers.date_normalizer import (
    DateNormalizer
)
from src.models.candidate import (
    RawCandidate,
    Location,
    Experience,
    Education
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

            experience = []

            for item in data.get("experience", []):

                experience.append(
                    Experience(
                        company=item.get("company"),
                        title=item.get("title"),
                        start=DateNormalizer.normalize(
                            item.get("start")
                        ),
                        end=DateNormalizer.normalize(
                            item.get("end")
                        ),
                        summary=item.get("summary")
                    )
                )

            education = []

            for item in data.get("education", []):

                education.append(
                    Education(
                        institution=item.get("institution"),
                        degree=item.get("degree"),
                        field=item.get("field"),
                        end_year=item.get("end_year")
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
            education=education,
            experience=experience,
            current_company=data.get("currentCompany"),
            current_title=data.get("jobTitle"),
            source="ATS_JSON"
        )