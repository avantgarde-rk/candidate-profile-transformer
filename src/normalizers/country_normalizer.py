class CountryNormalizer:

    COUNTRY_MAP = {
        "india": "IN",
        "united states": "US",
        "usa": "US",
        "united kingdom": "GB",
        "uk": "GB",
        "canada": "CA",
        "australia": "AU"
    }

    @staticmethod
    def normalize(country: str):

        if not country:
            return None

        return CountryNormalizer.COUNTRY_MAP.get(
            country.lower().strip(),
            country.upper()
        )