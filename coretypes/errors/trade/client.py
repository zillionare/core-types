import re
from typing import Any, Optional

from coretypes.errors.trade.base import ErrorCodes, TradeError
from coretypes.types import Frame


class BadParamsError(TradeError):
    """客户端参数错误异常"""

    error_code = ErrorCodes.ClientBadParams

    def __init__(self, msg: str, stack: Optional[str] = None):
        super().__init__(msg, stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        return {"msg": msg}


class AccountConflictError(TradeError):
    """账户冲突异常"""

    error_code = ErrorCodes.ClientAccountConflict

    def __init__(self, account: str, stack: Optional[str] = None):
        super().__init__(f"账户名{account}已被占用", stack)

    @classmethod
    def parse_msg(cls, account: str) -> dict:
        m = re.match(r"账户名(.*?)已被占用", account)
        return {
            "account": m.group(1),
        }


class AccountStoppedError(TradeError):
    """账户已停止异常"""

    error_code = ErrorCodes.ClientAccountStopped

    def __init__(self, bid_time: Frame, stop_time: Frame, stack: Optional[str] = None):
        super().__init__(f"下单时间为{bid_time},而账户已于{stop_time}冻结。", stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"下单时间为(.*?),而账户已于(.*?)冻结。", msg)
        return {"bid_time": m.group(1), "stop_time": m.group(2)}


class TimeRewindError(TradeError):
    """客户端时间回退异常"""

    error_code = ErrorCodes.ClientTimeRewind

    def __init__(self, cur: Frame, last_trade_time: Frame, stack: Optional[str] = None):
        super().__init__("委托时间必须递增出现。当前{cur}, 前一个委托时间{last_trade_time}", stack)

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        m = re.match(r"委托时间必须递增出现。当前(.*?), 前一个委托时间(.*?)", msg)
        return {
            "cur": m.group(1),
            "last_trade_time": m.group(2),
        }
