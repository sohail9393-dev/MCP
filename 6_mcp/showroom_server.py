from mcp.server.fastmcp import FastMCP
from showroom import CarShowroom

mcp = FastMCP("showroom_server")


# -------------------- BASIC INFO --------------------
@mcp.tool()
async def get_balance(name: str) -> float:
    """Get total revenue/balance of the showroom."""
    return CarShowroom.get(name).balance


@mcp.tool()
async def get_inventory(name: str) -> dict[str, int]:
    """Get available cars in inventory."""
    return CarShowroom.get(name).inventory


@mcp.tool()
async def get_maintenance(name: str) -> dict[str, int]:
    """Get cars currently under maintenance."""
    return CarShowroom.get(name).maintenance


# -------------------- OPERATIONS --------------------
@mcp.tool()
async def add_stock(name: str, model: str, quantity: int, price: float) -> str:
    """Add new cars to the showroom inventory.

    Args:
        name: Showroom name
        model: Car model
        quantity: Number of cars
        price: Purchase price
    """
    showroom = CarShowroom.get(name)
    showroom.add_stock(model, quantity, price)
    return "Stock added successfully"


@mcp.tool()
async def sell_car(name: str, model: str, quantity: int, price: float) -> str:
    """Sell cars from inventory.

    Args:
        name: Showroom name
        model: Car model
        quantity: Number of cars
        price: Selling price
    """
    return CarShowroom.get(name).sell_car(model, quantity, price)


@mcp.tool()
async def send_to_maintenance(name: str, model: str, quantity: int) -> str:
    """Send cars to maintenance.

    Args:
        name: Showroom name
        model: Car model
        quantity: Number of cars
    """
    CarShowroom.get(name).send_to_maintenance(model, quantity)
    return "Sent to maintenance"


@mcp.tool()
async def return_from_maintenance(name: str, model: str, quantity: int) -> str:
    """Return cars from maintenance to inventory."""
    CarShowroom.get(name).return_from_maintenance(model, quantity)
    return "Returned from maintenance"


# -------------------- REPORT --------------------
@mcp.tool()
async def get_showroom_value(name: str) -> float:
    """Get total showroom value (inventory + maintenance + balance)."""
    return CarShowroom.get(name).calculate_showroom_value()


# -------------------- RESOURCES --------------------
@mcp.resource("showroom://details/{name}")
async def read_showroom_resource(name: str) -> str:
    """Full showroom report"""
    showroom = CarShowroom.get(name.lower())
    return showroom.report()


@mcp.resource("showroom://inventory/{name}")
async def read_inventory_resource(name: str) -> str:
    showroom = CarShowroom.get(name.lower())
    return str(showroom.inventory)


@mcp.resource("showroom://maintenance/{name}")
async def read_maintenance_resource(name: str) -> str:
    showroom = CarShowroom.get(name.lower())
    return str(showroom.maintenance)


# -------------------- RUN SERVER --------------------
if __name__ == "__main__":
    mcp.run(transport='stdio')