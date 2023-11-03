import re
from typing import Optional

from coretypes.errors.trade.base import ErrorCodes, TradeError
from coretypes.types import Frame


class ServerNoDataForMatch(TradeError):
    """服务器无数据匹配异常"""

    error_code = ErrorCodes.ServerNoDataForMatch

    def __init__(self, security: str, order_time: Frame, stack: Optional[str] = None):
        super().__init__(f"没有匹配到{security}在{order_time}的成交数据", stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"没有匹配到(.*?)在(.*?)的成交数据", msg)
        return {
            "security": m.group(1),
            "order_time": m.group(2),
        }


class ServerNoData(TradeError):
    """服务器无数据异常"""

    error_code = ErrorCodes.ServerNoData

    def __init__(self, security: str, time: Frame, stack: Optional[str] = None):
        super().__init__(
            f"获取{security}在{time}的行情数据失败，请检查日期是否为交易日，或者当天是否停牌",
            stack,
        )

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"获取(.*?)在(.*?)的行情数据失败，请检查日期是否为交易日，或者当天是否停牌", msg)
        return {
            "security": m.group(1),
            "time": m.group(2),
        }
