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
from datetime import datetime

class MergeEngine:

    SOURCE_PRIORITY = {
        "ATS_JSON": 3,
        "RESUME_PDF": 2,
        "RECRUITER_CSV": 1
    }

    @staticmethod
    def calculate_years_experience(
        experience
    ) -> float | None:

        total_months = 0

        for item in experience:

            if not item.start:
                continue

            try:

                start_date = datetime.strptime(
                    item.start,
                    "%Y-%m"
                )

                if item.end:

                    end_date = datetime.strptime(
                        item.end,
                        "%Y-%m"
                    )

                else:

                    end_date = datetime.now()

                months = (
                    (end_date.year - start_date.year)
                    * 12
                    +
                    (end_date.month - start_date.month)
                )

                if months > 0:
                    total_months += months

            except ValueError:
                continue

        if total_months == 0:
            return None

        return round(
            total_months / 12,
            2
        )

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

        years_experience = (
            MergeEngine.calculate_years_experience(
                winner.experience
            )
        )

        selected_links = None

        for candidate in sorted_candidates:

            if candidate.links:
                selected_links = candidate.links
                break

        return CandidateProfile(
            candidate_id=candidate_id,
            full_name=winner.full_name,
            emails=winner.emails,
            phones=normalized_phones,
            location=winner.location,
            links=selected_links,
            headline=winner.current_title,
            years_experience=years_experience,
            skills=skills,
            experience=winner.experience,
            education=winner.education,
            provenance=provenance,
            overall_confidence=overall_confidence
        )