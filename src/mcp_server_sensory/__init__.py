"""
MCP Server Sensory - Multi-Sensory AI Communication
====================================================

Off-grid communication for AI systems using:
- Morse code (audio/visual/tactile)
- Braille (visual/tactile/punchcard)
- SSTV/Robot36 (images via audio)
- ggwave (ultrasonic data)

Part of HumoticaOS McMurdo Off-Grid Communication Layer.

Usage:
    from mcp_server_sensory import morse, braille

    # Encode message to Morse
    morse_msg = morse.encode("HELLO")  # .... . .-.. .-.. ---

    # Encode to Braille
    braille_msg = braille.encode("hello")  # ⠓⠑⠇⠇⠕

    # Create punchcard pattern
    pattern = braille.to_punchcard_pattern("hello")

One love, one fAmIly!
"""

__version__ = "0.1.0"

from .encoders import morse, braille

__all__ = ["morse", "braille", "__version__"]
