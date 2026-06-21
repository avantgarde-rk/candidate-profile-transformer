import pdfplumber
import re

from src.models.candidate import RawCandidate


class ResumeParser:

    EMAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    PHONE_PATTERN = r"(?:\+91[- ]?)?[6-9]\d{9}"

    COMMON_SKILLS = {
        "python",
        "java",
        "javascript",
        "react",
        "nodejs",
        "sql",
        "mysql",
        "aws",
        "docker",
        "git",
        "html",
        "css",
        "c",
        "c++"
    }

    @staticmethod
    def parse(file_path: str) -> RawCandidate:

        text = ""

        try:

            with pdfplumber.open(file_path) as pdf:

                for page in pdf.pages:

                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

        except Exception as e:

            raise ValueError(
                f"Invalid or corrupted PDF: {file_path}"
            ) from e

        # with pdfplumber.open(file_path) as pdf:
        #     for page in pdf.pages:
        #         extracted = page.extract_text()
        #         if extracted:
        #             text += extracted + "\n"

        emails = re.findall(
            ResumeParser.EMAIL_PATTERN,
            text
        )

        phones = [
            phone.strip()
            for phone in re.findall(
                ResumeParser.PHONE_PATTERN,
                text
            )
        ]

        skills_found = []

        lower_text = text.lower()

        for skill in ResumeParser.COMMON_SKILLS:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(
                pattern,
                lower_text
            ):
                skills_found.append(skill)

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        full_name = lines[0] if lines else None

        return RawCandidate(
            full_name=full_name,
            emails=list(set(emails)),
            phones=list(set(phones)),
            skills=skills_found,
            source="RESUME_PDF"
        )