from src.models.candidate import CandidateProfile
candidate = CandidateProfile(
    candidate_id="123",
    full_name="Rakesh"
)
print(candidate.model_dump())