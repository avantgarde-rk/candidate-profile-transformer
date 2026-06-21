from src.parsers.resume_parser import ResumeParser

candidate = ResumeParser.parse(
    "data/resumes/no_phone_resume.pdf"
)

print(candidate.model_dump())