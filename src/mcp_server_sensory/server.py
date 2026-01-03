"""
MCP Server Sensory - Multi-Sensory AI Communication Server
==========================================================

Provides tools for encoding/decoding messages across
multiple sensory modalities for off-grid AI communication.

Part of HumoticaOS McMurdo Off-Grid Communication Layer.
"""

import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from .encoders import morse, braille

# Create server instance
server = Server("sensory")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available sensory tools."""
    return [
        Tool(
            name="morse_encode",
            description="Encode text to Morse code. Formats: standard (.-), visual (█▄), binary (10)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to encode"},
                    "format": {
                        "type": "string",
                        "enum": ["standard", "visual", "binary"],
                        "default": "standard",
                        "description": "Output format"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="morse_decode",
            description="Decode Morse code back to text",
            inputSchema={
                "type": "object",
                "properties": {
                    "morse": {"type": "string", "description": "Morse code to decode"}
                },
                "required": ["morse"]
            }
        ),
        Tool(
            name="morse_timing",
            description="Get timing data for Morse audio/light generation",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to convert"},
                    "unit_ms": {"type": "integer", "default": 100, "description": "Base time unit in milliseconds"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="braille_encode",
            description="Encode text to Braille Unicode characters",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to encode"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="braille_decode",
            description="Decode Braille back to text",
            inputSchema={
                "type": "object",
                "properties": {
                    "braille": {"type": "string", "description": "Braille text to decode"}
                },
                "required": ["braille"]
            }
        ),
        Tool(
            name="braille_punchcard",
            description="Generate ASCII punchcard pattern from text - can be physically punched for audit trail!",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to convert"},
                    "cell_width": {"type": "integer", "default": 4, "description": "Width of each cell"},
                    "cell_height": {"type": "integer", "default": 6, "description": "Height of each cell"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="braille_binary_grid",
            description="Generate binary grid for machine-readable punchcard or CNC/laser cutting",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to convert"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="transcode",
            description="Convert between different sensory encodings",
            inputSchema={
                "type": "object",
                "properties": {
                    "input": {"type": "string", "description": "Input data"},
                    "from_format": {
                        "type": "string",
                        "enum": ["text", "morse", "braille"],
                        "description": "Source format"
                    },
                    "to_format": {
                        "type": "string",
                        "enum": ["text", "morse", "braille", "morse_visual", "punchcard"],
                        "description": "Target format"
                    }
                },
                "required": ["input", "from_format", "to_format"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""

    if name == "morse_encode":
        text = arguments["text"]
        fmt = arguments.get("format", "standard")
        format_enum = {
            "standard": morse.MorseFormat.STANDARD,
            "visual": morse.MorseFormat.VISUAL,
            "binary": morse.MorseFormat.BINARY
        }.get(fmt, morse.MorseFormat.STANDARD)

        result = morse.encode(text, format_enum)
        return [TextContent(type="text", text=result)]

    elif name == "morse_decode":
        morse_code = arguments["morse"]
        result = morse.decode(morse_code)
        return [TextContent(type="text", text=result)]

    elif name == "morse_timing":
        text = arguments["text"]
        unit_ms = arguments.get("unit_ms", 100)
        morse_code = morse.encode(text)
        timing = morse.to_timing(morse_code, unit_ms)
        return [TextContent(type="text", text=json.dumps(timing))]

    elif name == "braille_encode":
        text = arguments["text"]
        result = braille.encode(text)
        return [TextContent(type="text", text=result)]

    elif name == "braille_decode":
        braille_text = arguments["braille"]
        result = braille.decode(braille_text)
        return [TextContent(type="text", text=result)]

    elif name == "braille_punchcard":
        text = arguments["text"]
        cell_width = arguments.get("cell_width", 4)
        cell_height = arguments.get("cell_height", 6)
        result = braille.to_punchcard_pattern(text, cell_width, cell_height)
        return [TextContent(type="text", text=result)]

    elif name == "braille_binary_grid":
        text = arguments["text"]
        grid = braille.to_binary_grid(text)
        return [TextContent(type="text", text=json.dumps(grid))]

    elif name == "transcode":
        input_data = arguments["input"]
        from_fmt = arguments["from_format"]
        to_fmt = arguments["to_format"]

        # First convert to text
        if from_fmt == "morse":
            text = morse.decode(input_data)
        elif from_fmt == "braille":
            text = braille.decode(input_data)
        else:
            text = input_data

        # Then convert to target
        if to_fmt == "morse":
            result = morse.encode(text)
        elif to_fmt == "morse_visual":
            result = morse.encode(text, morse.MorseFormat.VISUAL)
        elif to_fmt == "braille":
            result = braille.encode(text)
        elif to_fmt == "punchcard":
            result = braille.to_punchcard_pattern(text)
        else:
            result = text

        return [TextContent(type="text", text=result)]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


def main():
    """Run the MCP server."""
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
