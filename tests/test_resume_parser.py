from src.models.candidate import RawCandidate
import re

with open(
    "data/resumes/sample_resume.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

emails = re.findall(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    text
)

phones = [
    p.strip()
    for p in re.findall(
        r"(?:\+91[- ]?)?[6-9]\d{9}",
        text
    )
]

print("Emails:", emails)
print("Phones:", phones)