from difflib import SequenceMatcher

from src.models.candidate import RawCandidate


class EntityMatcher:

    @staticmethod
    def names_similar(
        name1: str,
        name2: str
    ) -> bool:

        similarity = SequenceMatcher(
            None,
            name1.lower(),
            name2.lower()
        ).ratio()

        return similarity >= 0.85

    @staticmethod
    def is_same_candidate(
        candidate1: RawCandidate,
        candidate2: RawCandidate
    ) -> bool:

        # Email Match

        if (
            candidate1.emails
            and candidate2.emails
        ):
            if (
                candidate1.emails[0].lower()
                ==
                candidate2.emails[0].lower()
            ):
                return True

        # Phone Match

        if (
            candidate1.phones
            and candidate2.phones
        ):
            if (
                candidate1.phones[0]
                ==
                candidate2.phones[0]
            ):
                return True

        # Name Similarity

        if (
            candidate1.full_name
            and candidate2.full_name
        ):
            return EntityMatcher.names_similar(
                candidate1.full_name,
                candidate2.full_name
            )

        return False