from src.matching.entity_matcher import EntityMatcher

def test_name_similarity():

    assert EntityMatcher.names_similar(
        "Rakesh R",
        "Rakesh R."
    )

    assert not EntityMatcher.names_similar(
        "Rakesh R",
        "John Doe"
    )