import datetime
import unittest

from coretypes.errors.trade import *


class TradeErrorTest(unittest.TestCase):
    def test_from_json(self):
        d = {
            "error_code": 4000,
            "msg": "委托000002.XSHG在2018-03-29 14:32:00发生未知错误",
            "stack": "no more stack",
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, GenericError))

        d = {"error_code": 4001, "msg": "账户abced001资金不足, 需要3000.13, 当前12.35"}

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, CashError))

        d = {"error_code": 4002, "msg": "688788.XSHG委托价100.24达到，但成交量为零"}

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, VolumeNotMeet))

        d = {"error_code": 4003, "msg": "不能在涨停板上买入300325.XSHE, 2023-09-31"}

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, BuylimitError))

        d = {"error_code": 4004, "msg": "不能在跌停板上卖出300325.XSHE, 2023-09-31"}

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, SellLimitError))

        d = {"error_code": 4005, "msg": "000222.XSHE在2023-09-31期间没有持仓"}

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, PositionError))

        d = {"error_code": 4006, "msg": "300024在11:30之后未达到委托价:9.26"}

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, PriceNotMeet))

        d = {
            "error_code": 9999999,
            "msg": "委托000002.XSHG在2018-03-29 14:32:00发生未知错误",
            "stack": "no more stack",
        }
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, TradeError))
        self.assertEqual(e.stack, "no more stack")

        d = {
            "error_code": 4001,
            "msg": "委托000002.XSHG在2018-03-29 14:32:00发生未知错误",
            "stack": "no more stack",
        }
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, TradeError))

        # 异常对象构建时出错
        d = {
            "error_code": 4001,
            "msg": "委托在发生未知错误",
            "stack": "no more stack",
        }
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, TradeError))
        self.assertEqual(e.error_msg, "异常对象构建时出错。原错误代码：4001, 原错误消息：委托在发生未知错误")

    def test_as_json(self):
        e = CashError("fdgd", 1_000_000, 3_000, with_stack=True)
        print(e.stack)

        self.assertEqual(str(e), "4001: 账户fdgd资金不足, 需要1000000, 当前3000")
        d = e.as_json()
        del d["stack"]
        self.assertDictEqual(
            d,
            {"error_code": 4001, "msg": "账户fdgd资金不足, 需要1000000, 当前3000"},
        )

    def test_client_error(self):
        e = BadParamsError("传入参数错误(name), 要求test,实际为None")
        d = e.as_json()

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, BadParamsError))

        e = AccountConflictError("fdkgd")
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, AccountConflictError))

        bid_time = datetime.date(2022, 3, 1)
        stop_time = datetime.date(2022, 2, 28)
        e = AccountStoppedError(bid_time, stop_time)
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, AccountStoppedError))

        e = TimeRewindError(datetime.date(2022, 3, 1), datetime.date(2022, 3, 2))
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, TimeRewindError))

    def test_server_error(self):
        e = NoDataForMatch("000001", datetime.date(2022, 1, 1))
        d = e.as_json()
        d["stack"] = "mock call stack"
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, NoDataForMatch))
        self.assertEqual(d["stack"], "mock call stack")

        e = NoData("000001", datetime.date(2022, 1, 1))
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, NoData))

    def test_callstack(self):
        try:
            e = TradeError("this is a test", with_stack=True)
            raise e
        except TradeError as e:
            print(e.error_msg, e.error_code, e.stack)
