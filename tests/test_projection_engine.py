import json

from src.models.candidate import (
    CandidateProfile
)

from src.projection.projection_engine import (
    ProjectionEngine
)


def test_projection_engine():

    candidate = CandidateProfile(
        candidate_id="123",
        full_name="Rakesh",
        emails=["rakesh@gmail.com"],
        phones=["8610031411"],
        overall_confidence=0.95
    )

    with open(
        "configs/custom_config.json",
        "r",
        encoding="utf-8"
    ) as f:

        config = json.load(f)

    output = (
        ProjectionEngine.project(
            candidate,
            config
        )
    )

    assert (
        output["candidate_name"]
        == "Rakesh"
    )

    assert (
        output["primary_email"]
        ==
        "rakesh@gmail.com"
    )