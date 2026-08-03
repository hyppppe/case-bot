import json
import pathlib

from aiohttp import web

from auth import validate_init_data
from config import BOT_TOKEN, SPIN_COST
from db import get_or_create_user, get_balance, change_balance
from items import roll_item

STATIC_DIR = pathlib.Path(__file__).parent / "webapp" / "static"


def _user_from_parsed(parsed: dict) -> tuple[int, str | None]:
    user = json.loads(parsed["user"])
    return user["id"], user.get("username") or user.get("first_name")


async def _authenticate(request: web.Request) -> dict | None:
    body = await request.json()
    init_data = body.get("initData", "")
    return validate_init_data(init_data, BOT_TOKEN)


async def handle_me(request: web.Request) -> web.Response:
    parsed = await _authenticate(request)
    if parsed is None:
        return web.json_response({"error": "invalid init data"}, status=401)

    user_id, username = _user_from_parsed(parsed)
    balance = await get_or_create_user(user_id, username)
    return web.json_response({"balance": balance, "spin_cost": SPIN_COST})


async def handle_spin(request: web.Request) -> web.Response:
    parsed = await _authenticate(request)
    if parsed is None:
        return web.json_response({"error": "invalid init data"}, status=401)

    user_id, username = _user_from_parsed(parsed)
    await get_or_create_user(user_id, username)

    balance = await get_balance(user_id)
    if balance < SPIN_COST:
        return web.json_response({"error": "not enough coins"}, status=400)

    prize = roll_item()
    new_balance = await change_balance(user_id, prize["value"] - SPIN_COST)

    return web.json_response({"prize": prize, "balance": new_balance})


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/api/me", handle_me)
    app.router.add_post("/api/spin", handle_spin)
    app.router.add_static("/", path=STATIC_DIR, name="static", show_index=False)
    return app
