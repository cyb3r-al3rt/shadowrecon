"""
ShadowRecon v1.0 - Ultimate Web Attack Surface Discovery Framework
Developed by kernelpanic | A product of infosbios

"In the shadows, we find the truth. In reconnaissance, we find power."
"""

__version__ = "1.0.0"
__author__ = "kernelpanic | A product of infosbios"
__description__ = "Ultimate Web Attack Surface Discovery Framework"
__license__ = "MIT"

try:
    from .core.shadow_engine import ShadowEngine
    from .utils.colors import ShadowColors
    from .utils.banner import ShadowBanner
    __all__ = ['ShadowEngine', 'ShadowColors', 'ShadowBanner']
except ImportError:
    __all__ = []
