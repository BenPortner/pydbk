from pydbk import DBKScanner, default_destination
import argparse
import sys


class DBKCli:

    scanner: DBKScanner = None

    @classmethod
    def cli(cls, args=None):

        if args is None:
            args = ["--help"]

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
        parser.add_argument(
            "-t",
            "--mod-time",
            dest="mod_time",
            action="store_true",
            help="do not overwrite modification date of extracted files",
        )

        args = parser.parse_args(args)

        cls.scanner = DBKScanner(source=args.source)
        cls.scanner.extract_files(
            destination=args.destination,
            check_completeness=args.check,
            dry_run=args.dry_run,
            verbose=args.verbose,
            keep_modification_date=args.mod_time,
        )


cli = DBKCli.cli

if __name__ == "__main__":
    sys.exit(cli())
