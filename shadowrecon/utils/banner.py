"""
Banner and quote generation for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Shadow-themed banners and motivational quotes
"""

import random

class ShadowQuotes:
    """Inspirational shadow quotes for the interface"""

    QUOTES = [
        "In the shadows, we find the truth. In reconnaissance, we find power.",
        "Every shadow hides a vulnerability waiting to be discovered.",
        "The best reconnaissance happens in the silence between requests.",
        "In darkness, we see what others cannot. In shadows, we find what others miss.",
        "Attack surfaces are like shadows - they reveal themselves to those who know how to look.",
        "The deeper the shadow, the brighter the vulnerability shines.",
        "Patience is the shadow's greatest weapon. Persistence is its sharpest tool.",
        "In the realm of shadows, every endpoint tells a story.",
        "True power lies not in the light, but in understanding the darkness.",
        "Shadow reconnaissance: where silence speaks louder than noise.",
        "The art of shadow hunting: finding the invisible, testing the untestable.",
        "In every shadow lies an opportunity. In every opportunity lies a vulnerability.",
        "We are the shadows that dance between requests and responses.",
        "The hunt begins where others fear to tread - in the dark corners of the web.",
        "Shadow warriors don't just find vulnerabilities, they craft them from whispers.",
        "Every HTTP response is a shadow cast by the server's true intentions.",
        "In the shadow realm, payload is poetry and vulnerability is victory.",
        "We navigate the dark web of attack surfaces with the precision of shadows.",
        "The greatest discoveries happen in the space between what is and what could be.",
        "Shadow hunters: turning the invisible visible, the secure insecure."
    ]

    @classmethod
    def get_random_quote(cls) -> str:
        """Get a random shadow quote"""
        try:
            return random.choice(cls.QUOTES)
        except Exception:
            return "In the shadows, we find the truth."

class ShadowBanner:
    """ASCII banner generation for ShadowRecon"""

    @classmethod
    def generate_banner(cls) -> str:
        """Generate the main ShadowRecon banner"""

        try:
            from .colors import ShadowColors
        except ImportError:
            class ShadowColors:
                BRIGHT_PURPLE = BRIGHT_CYAN = BRIGHT_YELLOW = BRIGHT_GREEN = DIM = RESET = ''

        # Try pyfiglet for enhanced ASCII art
        try:
            import pyfiglet
            fonts = ['slant', 'shadow', 'doom', 'big', 'block']
            font = random.choice(fonts)
            ascii_art = pyfiglet.figlet_format("SHADOWRECON", font=font)

            enhanced_banner = [
                "",
                f"{ShadowColors.BRIGHT_PURPLE}{ascii_art}{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_CYAN}    Ultimate Web Attack Surface Discovery Framework{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_YELLOW}    Developed by kernelpanic | A product of infosbios{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_GREEN}    v1.0.0{ShadowColors.RESET}",
                "",
                f"{ShadowColors.DIM}💀 '{ShadowQuotes.get_random_quote()}'{ShadowColors.RESET}",
                ""
            ]
            return "\n".join(enhanced_banner)

        except ImportError:
            # Fallback to simple banner
            banner_lines = [
                "",
                f"{ShadowColors.BRIGHT_PURPLE}╔══════════════════════════════════════════════════════════════════════════╗{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_PURPLE}║                              🎭 SHADOWRECON v1.0                        ║{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_PURPLE}║            Ultimate Web Attack Surface Discovery Framework               ║{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_PURPLE}║            Developed by kernelpanic | A product of infosbios            ║{ShadowColors.RESET}",
                f"{ShadowColors.BRIGHT_PURPLE}╚══════════════════════════════════════════════════════════════════════════╝{ShadowColors.RESET}",
                "",
                f"{ShadowColors.DIM}💀 '{ShadowQuotes.get_random_quote()}'{ShadowColors.RESET}",
                ""
            ]
            return "\n".join(banner_lines)

    @classmethod
    def generate_section_banner(cls, title: str, width: int = 80) -> str:
        """Generate section banner"""
        try:
            from .colors import ShadowColors
        except ImportError:
            class ShadowColors:
                BRIGHT_PURPLE = RESET = ''

        if not isinstance(title, str):
            title = str(title)

        border = "═" * width

        return f"""
{ShadowColors.BRIGHT_PURPLE}{border}{ShadowColors.RESET}
{ShadowColors.BRIGHT_PURPLE}{title.center(width)}{ShadowColors.RESET}
{ShadowColors.BRIGHT_PURPLE}{border}{ShadowColors.RESET}
"""

    @classmethod
    def generate_vulnerability_banner(cls, vuln_type: str) -> str:
        """Generate vulnerability discovery banner"""
        try:
            from .colors import ShadowColors
        except ImportError:
            class ShadowColors:
                BRIGHT_RED = BRIGHT_YELLOW = RESET = ''

        return f"""
{ShadowColors.BRIGHT_RED}💀 VULNERABILITY DETECTED: {vuln_type.upper()} 💀{ShadowColors.RESET}
{ShadowColors.BRIGHT_YELLOW}Shadow Hunter has found something in the darkness...{ShadowColors.RESET}
"""

    @classmethod
    def get_simple_banner(cls) -> str:
        """Get simple banner without dependencies"""
        return """
🎭 SHADOWRECON v1.0
Ultimate Web Attack Surface Discovery Framework
Developed by kernelpanic | A product of infosbios

💀 'In the shadows, we find the truth...'
"""
