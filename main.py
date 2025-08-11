from fastmcp import FastMCP
from src.core.tools.tools import weather_mcp, calculator_mcp, youtube_transcript_mcp
from dotenv import load_dotenv


load_dotenv()
mcp = FastMCP("Weather & Calculator Bot 🌤️🧮")
mcp.mount(weather_mcp, prefix="weather")
mcp.mount(calculator_mcp, prefix="calculator")
mcp.mount(youtube_transcript_mcp, prefix="youtube")


if __name__ == "__main__":
    # Run the MCP server
    # Note: FastMCP handles timeouts internally for MCP protocol
    # Individual tool timeouts are configured in their respective modules
    mcp.run()