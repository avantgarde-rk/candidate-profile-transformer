from src.models.candidate import Provenance


class ProvenanceEngine:

    @staticmethod
    def create(
        field: str,
        source: str,
        method: str
    ) -> Provenance:

        return Provenance(
            field=field,
            source=source,
            method=method
        )