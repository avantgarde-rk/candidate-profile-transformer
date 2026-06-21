class ConfidenceEngine:

    SOURCE_CONFIDENCE = {
        "ATS_JSON": 0.95,
        "RESUME_PDF": 0.85,
        "RECRUITER_CSV": 0.80
    }

    @staticmethod
    def get_score(
        source: str
    ) -> float:

        return ConfidenceEngine.SOURCE_CONFIDENCE.get(
            source,
            0.50
        )