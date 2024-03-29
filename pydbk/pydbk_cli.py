from pydbk import DBKScanner
import argparse
import sys


class DBKCli:

    scanner: DBKScanner = None

    @classmethod
    def parser(cls):

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
            default=None,
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
            action="store_false",
            default=True,
            help="do not check if .dbk archive is complete",
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
            "--no-mod-time",
            dest="mod_time",
            action="store_false",
            default=True,
            help="do not restore file modification times",
        )

        return parser

    @classmethod
    def main(cls):
        args = cls.parser().parse_args()

        cls.scanner = DBKScanner(source=args.source)
        cls.scanner.extract_files(
            destination=args.destination,
            check_completeness=args.check,
            dry_run=args.dry_run,
            verbose=args.verbose,
            keep_modification_date=args.mod_time,
        )


cli = DBKCli.main


if __name__ == "__main__":
    sys.exit(cli())
