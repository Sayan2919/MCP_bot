from fastmcp import FastMCP
from src.core.tools.tools import weather_mcp, calculator_mcp
from dotenv import load_dotenv


load_dotenv()
mcp = FastMCP("Weather & Calculator Bot 🌤️🧮")
mcp.mount(weather_mcp, prefix="weather")
mcp.mount(calculator_mcp, prefix="calculator")


if __name__ == "__main__":
    mcp.run()