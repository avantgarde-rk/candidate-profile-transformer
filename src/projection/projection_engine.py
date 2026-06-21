class ProjectionEngine:

    @staticmethod
    def get_nested_value(
        data,
        path
    ):

        try:

            current = data

            parts = path.split(".")

            for part in parts:

                if "[" in part and "]" in part:

                    field = part.split("[")[0]

                    index = int(
                        part.split("[")[1]
                        .replace("]", "")
                    )

                    current = current[field][index]

                else:

                    current = current[part]

            return current

        except Exception:
            return None

    @staticmethod
    def project(
        candidate_profile,
        config
    ):

        profile_dict = (
            candidate_profile.model_dump()
        )

        output = {}

        for field_mapping in config["fields"]:

            target = field_mapping["path"]

            source = field_mapping["from"]

            value = (
                ProjectionEngine
                .get_nested_value(
                    profile_dict,
                    source
                )
            )

            if value is None:

                missing_policy = config.get(
                    "on_missing",
                    "null"
                )

                if missing_policy == "omit":
                    continue

                if missing_policy == "error":
                    raise ValueError(
                        f"Missing field: {source}"
                    )

            output[target] = value

        if config.get(
            "include_confidence",
            False
        ):
            output[
                "overall_confidence"
            ] = (
                candidate_profile
                .overall_confidence
            )

        if config.get(
            "include_provenance",
            False
        ):
            output[
                "provenance"
            ] = [
                p.model_dump()
                for p in candidate_profile
                .provenance
            ]

        return output