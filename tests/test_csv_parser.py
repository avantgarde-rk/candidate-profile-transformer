from src.parsers.csv_parser import CSVParser

candidate = CSVParser.parse(
    "data/recruiter/sample_recruiter.csv"
)

print(candidate.model_dump())