"""设备指纹相关接口。"""

from __future__ import annotations

from typing import Any


class DeviceAPI:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def guid(self) -> Any:
        return (await self._c.post("/api/QQLogin/GetDeviceGUID")).get("data")

    async def set_guid(self, guid: str) -> None:
        await self._c.post("/api/QQLogin/SetDeviceGUID", {"guid": guid})

    async def mac(self) -> Any:
        return (await self._c.post("/api/QQLogin/GetLinuxMAC")).get("data")

    async def machine_id(self) -> Any:
        return (await self._c.post("/api/QQLogin/GetLinuxMachineId")).get("data")
