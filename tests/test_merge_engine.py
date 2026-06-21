from src.models.candidate import RawCandidate
from src.merger.merge_engine import MergeEngine


def test_merge_engine():

    ats = RawCandidate(
        full_name="Rakesh",
        emails=["rakesh@gmail.com"],
        phones=["8610031411"],
        skills=["Python"],
        source="ATS_JSON"
    )

    resume = RawCandidate(
        skills=["React"],
        source="RESUME_PDF"
    )

    merged = MergeEngine.merge(
        [ats, resume]
    )

    assert merged.full_name == "Rakesh"

    assert merged.emails == [
        "rakesh@gmail.com"
    ]

    assert len(
        merged.skills
    ) == 2

    assert (
        merged.overall_confidence
        == 0.95
    )