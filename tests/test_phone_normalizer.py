from src.normalizers.phone_normalizer import PhoneNormalizer


def test_phone_normalization():

    assert (
        PhoneNormalizer.normalize("8610031411")
        ==
        "+918610031411"
    )

    assert (
        PhoneNormalizer.normalize("+91 8610031411")
        ==
        "+918610031411"
    )