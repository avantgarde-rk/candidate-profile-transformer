from src.parsers.ats_parser import ATSParser
from src.parsers.resume_parser import ResumeParser
from src.merger.merge_engine import MergeEngine

ats = ATSParser.parse(
    "data/ats/test_priority_ats.json"
)

resume = ResumeParser.parse(
    "data/resumes/test_priority_resume.pdf"
)

merged = MergeEngine.merge(
    [ats, resume]
)

for skill in merged.skills:
    print(skill.name)