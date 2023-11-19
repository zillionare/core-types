import io
import traceback
from enum import IntEnum
from typing import Optional


class ErrorCodes(IntEnum):
    Unknown = 1000

    ClientGeneric = 2000
    ClientBadParams = 2001
    ClientAccountConflict = 2002
    ClientAccountStopped = 2003
    ClientTimeRewind = 2004

    ServerGeneric = 3000
    ServerNoDataForMatch = 3001
    ServerNoData = 3002

    TradeGeneric = 4000
    TradeNoCash = 4001
    TradeVolNotEnough = 4002
    TradeReachBuyLimit = 4003
    TradeReachSellLimit = 4004
    TradeNoPosition = 4005
    TradePirceNotMeet = 4006


class TradeError(Exception):
    """交易错误基类

    在交易和回测过程产生的各种异常，包括客户端参数错误、账户错误、交易限制等。由于需要本异常信息可能需要从服务器传递到客户端并重建，所以需要有串行化能力（使用json)，以及需要传递callstack trace.
    """

    error_code = ErrorCodes.Unknown

    def __init__(self, msg: str, with_stack: bool = False):
        self.error_msg = msg
        self.stack = None
        if with_stack:
            buffer = io.StringIO()
            traceback.print_stack(file=buffer, limit=20)
            stack = buffer.getvalue()

            # last 2 lines are print_stack and etc.
            self.stack = "\n".join(stack.split("\n")[:-2])

    @classmethod
    def parse_msg(cls, msg: str) -> dict:
        raise NotImplementedError

    @classmethod
    def from_json(cls, e: dict):
        """从json字符串中重建错误对象"""
        error_code = e["error_code"]
        error_msg = e["msg"]
        stack = e.get("stack")

        for klass in cls.__subclasses__():
            if klass.error_code.value == error_code:
                try:
                    obj = klass(**klass.parse_msg(error_msg))
                    if stack is not None:
                        obj.stack = stack

                    return obj
                except Exception:
                    te = TradeError(f"异常对象构建时出错。原错误代码：{error_code}, 原错误消息：{error_msg}")
                    te.stack = stack
                    return te
        else:
            te = TradeError(f"未知错误类型。错误代码: {error_code}, 错误消息为{error_msg}")
            te.stack = stack
            return te

    def as_json(self):
        """将对象串行化为json字符串，以遍可以通过网络传输"""
        if self.stack is not None:
            return {
                "error_code": self.error_code.value,
                "msg": self.error_msg,
                "stack": self.stack,
            }
        else:
            return {
                "error_code": self.error_code.value,
                "msg": self.error_msg,
            }

    def __str__(self):
        return f"{self.error_code}: {self.error_msg}"
