# -*- coding: utf-8 -*-
import pytest

from DisplayCAL.argyll_RGB2XYZ import RGB2XYZ, XYZ2RGB

pytest.skip(allow_module_level=True)
@pytest.mark.parametrize("colorspace", ("RGB", "XYZ"))
def test_agryll_colorspace_conversion(colorspace: str) -> None:
    """Test value conversion between RGB and XYZ colorspace."""
    for RGB, XYZ in iter(
        (
            ((1.0, 1.0, 1.0), (0.951065, 1.000000, 1.088440)),
            ((0.0, 0.0, 0.0), (0.010000, 0.010000, 0.010000)),
            ((0.5, 0.0, 0.0), (0.097393, 0.055060, 0.014095)),
            ((1.0, 0.0, 0.0), (0.418302, 0.220522, 0.029132)),
            ((0.0, 0.5, 0.0), (0.085782, 0.161542, 0.035261)),
            ((0.5, 0.5, 0.0), (0.173175, 0.206603, 0.039356)),
            ((1.0, 0.5, 0.0), (0.494083, 0.372064, 0.054393)),
            ((0.0, 1.0, 0.0), (0.364052, 0.718005, 0.128018)),
            ((0.5, 1.0, 0.0), (0.451445, 0.763065, 0.132113)),
            ((1.0, 1.0, 0.0), (0.772354, 0.928527, 0.147151)),
            ((0.0, 0.0, 0.5), (0.048252, 0.025298, 0.211475)),
            ((0.5, 0.0, 0.5), (0.135645, 0.070358, 0.215570)),
            ((1.0, 0.0, 0.5), (0.456553, 0.235820, 0.230607)),
            ((0.0, 0.5, 0.5), (0.124033, 0.176840, 0.236735)),
            ((0.5, 0.5, 0.5), (0.211427, 0.221901, 0.240831)),
            ((1.0, 0.5, 0.5), (0.532335, 0.387362, 0.255868)),
            ((0.0, 1.0, 0.5), (0.402304, 0.733303, 0.329493)),
            ((0.5, 1.0, 0.5), (0.489697, 0.778364, 0.333588)),
            ((1.0, 1.0, 0.5), (0.810605, 0.943825, 0.348625)),
            ((0.0, 0.0, 1.0), (0.188711, 0.081473, 0.951290)),
            ((0.5, 0.0, 1.0), (0.276104, 0.126533, 0.955385)),
            ((1.0, 0.0, 1.0), (0.597013, 0.291995, 0.970422)),
            ((0.0, 0.5, 1.0), (0.264493, 0.233015, 0.976550)),
            ((0.5, 0.5, 1.0), (0.351886, 0.278076, 0.980645)),
            ((1.0, 0.5, 1.0), (0.672794, 0.443537, 0.995683)),
            ((0.0, 1.0, 1.0), (0.542763, 0.789478, 1.069308)),
            ((0.5, 1.0, 1.0), (0.630157, 0.834539, 1.073403)),
        )
    ):
        if colorspace == "RGB":
            conversion = tuple(str(round(c, 6)) for c in RGB2XYZ(*RGB))
            result = tuple(str(c) for c in XYZ)
        else:
            conversion = tuple(str(round(c, 1)) for c in XYZ2RGB(*XYZ))
            result = tuple(str(c) for c in RGB)
        assert conversion == result
