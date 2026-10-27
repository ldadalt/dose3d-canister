"""3D dose reconstruction inside a blood-irradiator canister."""

from dose3d_canister.criteria import BCSH, FDA_AABB, JAPAN, PORTARIA_158
from dose3d_canister.geometry import GAMMACELL_3000_ELAN

__version__ = "0.1.0"
__all__ = [
    "BCSH",
    "FDA_AABB",
    "GAMMACELL_3000_ELAN",
    "JAPAN",
    "PORTARIA_158",
    "__version__",
]
