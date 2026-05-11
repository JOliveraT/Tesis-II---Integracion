import httpx


async def get_json(url: str, *, params: dict | None = None, headers: dict | None = None) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


async def post_form(url: str, *, data: dict) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, data=data)
        response.raise_for_status()
        return response.json()
