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

        d = {
            "error_code": 4001,
            "msg": "账户abced001资金不足, 需要3000.13, 当前12.35",
            "stack": None,
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, NocashError))

        d = {
            "error_code": 4002,
            "msg": "688788.XSHG委托价100.24达到，但成交量为零",
            "stack": None,
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, VolumeNotMeet))

        d = {
            "error_code": 4003,
            "msg": "不能在涨停板上买入300325.XSHE, 2023-09-31",
            "stack": None,
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, BuylimitError))

        d = {
            "error_code": 4004,
            "msg": "不能在跌停板上卖出300325.XSHE, 2023-09-31",
            "stack": None,
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, SellLimitError))

        d = {
            "error_code": 4005,
            "msg": "000222.XSHE在2023-09-31期间没有持仓",
            "stack": None,
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, NopositionError))

        d = {
            "error_code": 4006,
            "msg": "300325.XSHE现价未达到委托价:10.26",
            "stack": None,
        }

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, PriceNotMeet))

        d = {
            "error_code": 4000000,
            "msg": "委托000002.XSHG在2018-03-29 14:32:00发生未知错误",
            "stack": "no more stack",
        }
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, TradeError))

        d = {
            "error_code": 4001,
            "msg": "委托000002.XSHG在2018-03-29 14:32:00发生未知错误",
            "stack": "no more stack",
        }
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, TradeError))

    def test_as_json(self):
        e = NocashError("fdgd", 1_000_000, 3_000)

        self.assertEqual(str(e), "4001: 账户fdgd资金不足, 需要1000000, 当前3000")
        d = e.as_json()
        self.assertDictEqual(
            d,
            {
                "error_code": 4001,
                "msg": "账户fdgd资金不足, 需要1000000, 当前3000",
                "stack": None,
            },
        )

    def test_client_error(self):
        e = ClientBadParamsError("传入参数错误(name), 要求test,实际为None")
        d = e.as_json()

        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, ClientBadParamsError))

        e = ClientAccountConflictError("fdkgd")
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, ClientAccountConflictError))

        e = ClientAccountStoppedError("fdkgd")
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, ClientAccountStoppedError))

        e = ClientTimeRewindError(datetime.date(2022, 3, 1), datetime.date(2022, 3, 2))
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, ClientTimeRewindError))

    def test_server_error(self):
        e = ServerNoDataForMatch("000001", datetime.date(2022, 1, 1))
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, ServerNoDataForMatch))

        e = ServerNoData("000001", datetime.date(2022, 1, 1))
        d = e.as_json()
        e = TradeError.from_json(d)
        self.assertTrue(isinstance(e, ServerNoData))
