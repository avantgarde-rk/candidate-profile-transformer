import argparse

from src.utils.pipeline import (
    CandidatePipeline
)


def main():

    parser = argparse.ArgumentParser(
        description="Candidate Profile Transformer"
    )

    parser.add_argument(
        "--ats",
        required=True,
        help="Path to ATS JSON file"
    )

    parser.add_argument(
        "--resume",
        required=True,
        help="Path to Resume PDF file"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to Recruiter CSV file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to Projection Config"
    )

    args = parser.parse_args()

    try:

        output, errors = (
            CandidatePipeline.run(
                ats_path=args.ats,
                resume_path=args.resume,
                csv_path=args.csv,
                config_path=args.config
            )
        )

        print("\nOUTPUT\n")
        print(output)

        print("\nVALIDATION\n")
        print(errors)

    except Exception as e:

        print("\nERROR\n")
        print(str(e))


if __name__ == "__main__":
    main()