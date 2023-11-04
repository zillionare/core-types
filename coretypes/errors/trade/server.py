import re

from coretypes.errors.trade.base import ErrorCodes, TradeError
from coretypes.types import Frame


class NoDataForMatch(TradeError):
    """服务器无数据匹配异常"""

    error_code = ErrorCodes.ServerNoDataForMatch

    def __init__(self, security: str, order_time: Frame, with_stack: bool = False):
        super().__init__(f"没有匹配到{security}在{order_time}的成交数据", with_stack=with_stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"没有匹配到(.*?)在(.*?)的成交数据", msg)
        return {
            "security": m.group(1),  # type: ignore
            "order_time": m.group(2),  # type: ignore
        }


class NoData(TradeError):
    """服务器无数据异常"""

    error_code = ErrorCodes.ServerNoData

    def __init__(self, security: str, time: Frame, with_stack: bool = False):
        super().__init__(
            f"获取{security}在{time}的行情数据失败，请检查日期是否为交易日，或者当天是否停牌", with_stack=with_stack
        )

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"获取(.*?)在(.*?)的行情数据失败，请检查日期是否为交易日，或者当天是否停牌", msg)
        return {
            "security": m.group(1),  # type: ignore
            "time": m.group(2),  # type: ignore
        }
