from src.normalizers.skill_normalizer import SkillNormalizer


def test_skill_normalization():

    assert (
        SkillNormalizer.normalize("JS")
        ==
        "JavaScript"
    )

    assert (
        SkillNormalizer.normalize("Javascript")
        ==
        "JavaScript"
    )

    assert (
        SkillNormalizer.normalize("python")
        ==
        "Python"
    )