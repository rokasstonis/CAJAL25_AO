import numpy as np
from pathlib import Path
from settings.settings import exp_dir
import os


def generate_yaml_file(mXLocationPixels, mYLocationPixels, mPowerDensity, mRadiusPixels):
    output_path = exp_dir / "output_regions.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write("---\n")
        for x, y in zip(mXLocationPixels, mYLocationPixels):
            f.write(
                "StartClass:\n"
                "  ClassName: CStimulationRegionSpecification\n"
                f"  mPowerDensity: {mPowerDensity}\n"
                f"  mRadiusPixels: {mRadiusPixels}\n"
                f"  mXLocationPixels: {x}\n"
                f"  mYLocationPixels: {y}\n"
                "  mZPlane: 0\n"
                "EndClass: CStimulationRegionSpecification\n"
            )
        f.write("...\n")