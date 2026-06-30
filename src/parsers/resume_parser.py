import pdfplumber
import re

from src.models.candidate import (
    RawCandidate,
    Links
)

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

    URL_PATTERN = (
        r"(?:https?://)?(?:www\.)?"
        r"(?:linkedin\.com/[^\s,]+|github\.com/[^\s,]+|"
        r"[\w.-]+\.(?:com|dev|app|io|ai|in)/?[^\s,]*)"
    )

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

        urls = re.findall(
            ResumeParser.URL_PATTERN,
            text
        )

        linkedin = None
        github = None
        portfolio = None
        other_links = []

        for url in urls:

            clean_url = url.strip().rstrip(".,)")
            if "@" in clean_url:
                continue

            lower_url = clean_url.lower()

            if "linkedin.com" in lower_url:
                linkedin = clean_url

            elif "github.com" in lower_url:
                github = clean_url

            elif (
                "portfolio" in lower_url
                or "vercel.app" in lower_url
                or "netlify.app" in lower_url
            ):
                portfolio = clean_url

            else:
                other_links.append(clean_url)

        links = None

        if linkedin or github or portfolio or other_links:

            links = Links(
                linkedin=linkedin,
                github=github,
                portfolio=portfolio,
                other=other_links
            )

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
            links=links,
            source="RESUME_PDF"
        )