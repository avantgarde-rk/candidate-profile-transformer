from src.models.candidate import RawCandidate
from src.matching.entity_matcher import EntityMatcher


def test_entity_matching():

    candidate1 = RawCandidate(
        full_name="John Doe",
        emails=["john@gmail.com"],
        source="ATS_JSON"
    )

    candidate2 = RawCandidate(
        full_name="Jon Doe",
        emails=["john@gmail.com"],
        source="RESUME_PDF"
    )

    assert (
        EntityMatcher.is_same_candidate(
            candidate1,
            candidate2
        )
        is True
    )