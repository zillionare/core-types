import re
from typing import Optional

from coretypes.errors.trade.base import ErrorCodes, TradeError
from coretypes.types import Frame


class GenericError(TradeError):
    """原因不明的委托错误"""

    error_code = ErrorCodes.TradeGeneric

    def __init__(self, security: str, time: Frame, with_stack: bool=False):
        super().__init__(f"委托{security}在{time}发生未知错误", with_stack=with_stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"委托(.*?)在(.*?)发生未知错误", msg)
        return {
            "security": m.group(1),  # type: ignore
            "time": m.group(2),  # type: ignore
        }


class CashError(TradeError):
    """账户余额不足"""

    error_code = ErrorCodes.TradeNoCash

    def __init__(
        self,
        account: str,
        required: float,
        available: float,
        with_stack: bool = False,
    ):
        super().__init__(
            f"账户{account}资金不足, 需要{required}, 当前{available}", with_stack=with_stack
        )

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"账户(.*?)资金不足, 需要(\d+(\.\d+)?), 当前(\d+(\.\d+)?)", msg)
        return {
            "account": m.group(1),  # type: ignore
            "required": float(m.group(2)),  # type: ignore
            "available": float(m.group(3)),  # type: ignore
        }


class BuylimitError(TradeError):
    """不允许涨停板上买入"""

    error_code = ErrorCodes.TradeReachBuyLimit

    def __init__(self, security: str, time: Frame, with_stack: bool = False):
        super().__init__(f"不能在涨停板上买入{security}, {time}", with_stack=with_stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"不能在涨停板上买入(.*?), (.*?)", msg)
        return {
            "security": m.group(1),  # type: ignore
            "time": m.group(2),  # type: ignore
        }


class SellLimitError(TradeError):
    """不允许跌停板上卖出"""

    error_code = ErrorCodes.TradeReachSellLimit

    def __init__(self, security: str, time: Frame, with_stack: bool = False):
        super().__init__(f"不能在跌停板上卖出{security}, {time}", with_stack=with_stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"不能在跌停板上卖出(.*?), (.*?)", msg)
        return {
            "security": m.group(1),  # type: ignore
            "time": m.group(2),  # type: ignore
        }


class PositionError(TradeError):
    """`security`在期间没有持仓时发出卖出指令"""

    error_code = ErrorCodes.TradeNoPosition

    def __init__(self, security: str, time: Frame, with_stack: bool = False):
        super().__init__(f"{security}在{time}期间没有持仓", with_stack=with_stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"(.*?)在(.*?)期间没有持仓", msg)
        return {
            "security": m.group(1),  # type: ignore
            "time": m.group(2),  # type: ignore
        }


class PriceNotMeet(TradeError):
    """`security`现价未达到委托价，无法成交"""

    error_code = ErrorCodes.TradePirceNotMeet

    def __init__(
        self, security: str, price: float, order_time: Frame, with_stack: bool = False
    ):

        super().__init__(
            f"{security}在{order_time}之后未达到委托价:{price}", with_stack=with_stack
        )

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"(.*?)在(.*?)之后未达到委托价:(\d+(\.\d+)?)", msg)
        return {
            "security": m.group(1),  # type: ignore
            "order_time": m.group(2),  # type: ignore
            "price": float(m.group(3)),  # type: ignore
        }


class VolumeNotMeet(TradeError):
    """`security`委托价达到，但成交量为零。"""

    error_code = ErrorCodes.TradeVolNotEnough

    def __init__(self, security: str, price: float, with_stack: bool = False):
        super().__init__(f"{security}委托价{price}达到，但成交量为零", with_stack=with_stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"(.*?)委托价(\d+(\.\d+)?)达到，但成交量为零", msg)
        return {
            "security": m.group(1),  # type: ignore
            "price": float(m.group(2)),  # type: ignore
        }
