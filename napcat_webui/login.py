"""登录相关接口。"""

from __future__ import annotations

from typing import Any


class LoginAPI:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def status(self) -> Any:
        """查询登录阶段：loginPhase / isLogin / isOffline / coreReady 等。"""
        return (await self._c.post("/api/QQLogin/CheckLoginStatus")).get("data")

    async def qrcode(self, refresh: bool = False) -> str | None:
        """返回当前登录二维码链接；refresh=True 时强制刷新。"""
        endpoint = "/api/QQLogin/RefreshQRcode" if refresh else "/api/QQLogin/GetQQLoginQrcode"
        data = (await self._c.post(endpoint)).get("data") or {}
        return data.get("qrcodeurl") or data.get("qrcode")

    async def quick_login_list(self) -> Any:
        return (await self._c.post("/api/QQLogin/GetQuickLoginList")).get("data")

    async def quick_login_list_new(self) -> Any:
        return (await self._c.post("/api/QQLogin/GetQuickLoginListNew")).get("data")

    async def set_quick_login(self, uin: int | str) -> None:
        await self._c.post("/api/QQLogin/SetQuickLogin", {"uin": uin})
