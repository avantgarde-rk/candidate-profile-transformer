from src.parsers.ats_parser import ATSParser

candidate = ATSParser.parse(
    "data/ats/sample_ats.json"
)

print(candidate.model_dump())