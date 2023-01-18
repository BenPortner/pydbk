from pydbk import extract_files, default_destination
import argparse
import sys


def pydbk_cli(args=None):

    parser = argparse.ArgumentParser(
        description="Pydbk: A Python tool to extract .dbk archives."
    )
    parser.add_argument(
        "source", type=str, help="source file to extract files from (.dbk)"
    )
    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default=default_destination,
        help=f"destination directory to extract files to",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose mode (print detailed output)",
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="check if .dbk archive is complete",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="run program without writing files to the destination",
    )

    args = parser.parse_args(args)

    extract_files(
        source=args.source,
        destination=args.destination,
        check_completeness=args.check,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    sys.exit(pydbk_cli())
