import hashlib

from src.models.candidate import (
    CandidateProfile,
    Skill,
    RawCandidate,
)
from src.provenance.provenance_engine import (
    ProvenanceEngine
)
from src.confidence.confidence_engine import (
    ConfidenceEngine
)

from src.normalizers.skill_normalizer import (
    SkillNormalizer
)

from src.normalizers.phone_normalizer import (
    PhoneNormalizer
)

class MergeEngine:

    SOURCE_PRIORITY = {
        "ATS_JSON": 3,
        "RESUME_PDF": 2,
        "RECRUITER_CSV": 1
    }

    @staticmethod
    def merge(
        candidates: list[RawCandidate]
    ) -> CandidateProfile:

        sorted_candidates = sorted(
            candidates,
            key=lambda c:
            MergeEngine.SOURCE_PRIORITY.get(
                c.source,
                0
            ),
            reverse=True
        )

        winner = sorted_candidates[0]

        # Deterministic ID

        base_string = (
            (winner.full_name or "")
            +
            (
                winner.emails[0]
                if winner.emails
                else ""
            )
        )

        candidate_id = hashlib.sha256(
            base_string.encode()
        ).hexdigest()[:12]

        # Skills + Sources

        skill_sources = {}

        for candidate in candidates:

            for skill in candidate.skills:

                normalized_skill = (
                    SkillNormalizer.normalize(
                        skill
                    )
                )

                skill_sources.setdefault(
                    normalized_skill,
                    []
                ).append(
                    candidate.source
                )

        skills = []

        for skill_name in sorted(
            skill_sources.keys()
        ):

            confidence = max(
                ConfidenceEngine.get_score(
                    source
                )
                for source in skill_sources[
                    skill_name
                ]
            )

            skills.append(
                Skill(
                    name=skill_name,
                    confidence=confidence,
                    sources=skill_sources[
                        skill_name
                    ]
                )
            )

        # Provenance

        provenance = []

        provenance.append(
            ProvenanceEngine.create(
                field="full_name",
                source=winner.source,
                method="source_priority"
            )
        )

        provenance.append(
            ProvenanceEngine.create(
                field="emails",
                source=winner.source,
                method="source_priority"
            )
        )

        provenance.append(
            ProvenanceEngine.create(
                field="phones",
                source=winner.source,
                method="source_priority"
            )
        )

        # Overall confidence

        overall_confidence = (
            ConfidenceEngine.get_score(
                winner.source
            )
        )

        normalized_phones = []

        for phone in winner.phones:

            normalized = (
                PhoneNormalizer.normalize(phone)
            )

            if normalized:
                normalized_phones.append(
                    normalized
                )

        return CandidateProfile(
            candidate_id=candidate_id,
            full_name=winner.full_name,
            emails=winner.emails,
            phones=normalized_phones,
            location=winner.location,
            skills=skills,
            provenance=provenance,
            overall_confidence=overall_confidence
        )