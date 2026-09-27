"""Run an interactive experiment or a deterministic smoke experiment."""

import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m coop_navigation_sds",
        description="Configure a speech-dialogue experiment, or use --smoke to check the pipeline without models or audio playback.",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run a fast deterministic pipeline without opening the configuration GUI",
    )
    parser.add_argument(
        "--results-dir",
        default=None,
        help="top-level result directory used by --smoke",
    )
    arguments = parser.parse_args(argv)
    if arguments.results_dir is not None and not arguments.smoke:
        parser.error("--results-dir applies to --smoke; configure experiment output in the startup dialog for a full run")
    if arguments.smoke:
        from coop_navigation_sds.smoke import run_smoke

        try:
            result, paths = run_smoke(arguments.results_dir or "results")
        except (OSError, ValueError, RuntimeError) as error:
            print(f"Smoke check failed: {error}", file=sys.stderr)
            return 1
        print(f"Smoke result: {result.extra.get('conversation_outcome', 'unknown')}")
        print(f"Run folder: {paths['run_dir']}")
    else:
        from coop_navigation_sds.app import main as run_interactive

        run_interactive()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
