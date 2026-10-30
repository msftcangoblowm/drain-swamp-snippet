from typing import (
    Any,
    TypeGuard,
)

__all__ = ("is_ok",)

def is_ok(test: Any | None) -> TypeGuard[str]: ...
