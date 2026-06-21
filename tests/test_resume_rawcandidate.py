from src.parsers.resume_parser import ResumeParser

candidate = ResumeParser.parse(
    "data/resumes/RakeshResume.pdf"
)

print(candidate.model_dump())