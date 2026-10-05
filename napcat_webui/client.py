"""NapCat WebUI 异步客户端。

负责鉴权握手与 Bearer 注入；业务接口在 login / device 子模块中。
"""

from __future__ import annotations

import httpx

from .auth import compute_hash
from .device import DeviceAPI
from .login import LoginAPI


class Client:
    def __init__(self, base_url: str, token: str, timeout: float = 15.0) -> None:
        self._base = base_url.rstrip("/")
        self._token = token
        self._credential: str | None = None
        self._http = httpx.AsyncClient(base_url=self._base, timeout=timeout)
        self.login = LoginAPI(self)
        self.device = DeviceAPI(self)

    async def __aenter__(self) -> "Client":
        await self.authenticate()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    async def authenticate(self) -> str:
        """执行一次登录握手，刷新并缓存 Credential。"""
        r = await self._http.post(
            "/api/auth/login",
            json={"hash": compute_hash(self._token), "totpCode": ""},
        )
        r.raise_for_status()
        payload = r.json()
        if payload.get("code") not in (0, None):
            raise RuntimeError(f"登录失败: {payload}")
        credential = (payload.get("data") or {}).get("Credential")
        if not credential:
            raise RuntimeError("登录成功但未返回 Credential")
        self._credential = credential
        return credential

    async def post(self, path: str, json: dict | None = None) -> dict:
        """带 Bearer 的 POST；遇到 401/403 自动重新登录一次并重放。"""
        if self._credential is None:
            await self.authenticate()
        r = await self._post_once(path, json)
        if r.status_code in (401, 403):
            await self.authenticate()
            r = await self._post_once(path, json)
        r.raise_for_status()
        payload = r.json()
        if isinstance(payload, dict) and payload.get("code") not in (0, None):
            raise RuntimeError(f"{path} 返回错误: {payload.get('message')}")
        return payload

    async def _post_once(self, path: str, json: dict | None) -> httpx.Response:
        headers = {"Authorization": f"Bearer {self._credential}"}
        return await self._http.post(path, json=json, headers=headers)

    async def close(self) -> None:
        await self._http.aclose()
