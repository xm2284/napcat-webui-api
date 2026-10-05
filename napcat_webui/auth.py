"""WebUI 鉴权哈希。

NapCat WebUI 使用一个确定性哈希作为登录凭据：
    hash = SHA256(token + ".napcat")
这里只做纯计算，不涉及网络。
"""

from __future__ import annotations

import hashlib


def compute_hash(token: str) -> str:
    """返回 WebUI 登录所需的十六进制哈希。"""
    if not token:
        raise ValueError("token 不能为空")
    return hashlib.sha256(f"{token}.napcat".encode("utf-8")).hexdigest()
