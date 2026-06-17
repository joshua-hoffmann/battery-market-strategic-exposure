from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_step(script_name: str) -> None:
    script_path = PROJECT_ROOT / "src" / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Missing pipeline script: {script_path}")

    print("")
    print(f"Running: {script_path.name}")
    subprocess.run([sys.executable, str(script_path)], cwd=str(PROJECT_ROOT), check=True)


def main() -> None:
    run_step("calculate_exposure_indicators.py")
    run_step("create_charts.py")
    print("")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
