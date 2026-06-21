from src.parsers.ats_parser import ATSParser

candidate = ATSParser.parse(
    "data/ats/test_location.json"
)

print(candidate.model_dump())