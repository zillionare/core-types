# zillionare core types


<p align="center">
<a href="https://pypi.python.org/pypi/zillionare_core_types">
    <img src="https://img.shields.io/pypi/v/zillionare_core_types.svg"
        alt = "Release Status">
</a>
<a href="#">
    <img src="https://github.com/zillionare/core-types/actions/workflows/release.yml/badge.svg" alt="CI status"/>
</a>
</p>

## Usage
To use zillionare core types in a project

```
    from coretypes import Frame, FrameType
```

## Features

本模块提供了在 Zillionare 中的核心类型定义。主要有：

1. 基础数据结构类的定义，比如时间帧类型 FrameType （对应于其它框架中可能使用的字符串 '1m', '1d'之类的定义）， 时间日期类型 Frame， 证券类型定义 FrameType 等。在几乎所有需要使用行情数据的地方，您都应该使用这些类型定义。
2. 交易错误类型，比如 NocashError （现金不足以完成交易错误）等等。
3. QuotesFetcher 接口定义。如果您要将其它数据源接入到 zillionare 中，就需要实现这个接口，按照定义返回相应的数据。一旦实现了此接口，就可以在 zillionare-omega 配置文件中配置接口，以例 omega 可以自动启用这个 adaptor 来获取数据。

### 基础数据结构定义

基础数据结构定义中，共有两种类型。一种是用以静态类型检查使用的，通常 IDE，mypy 这样一些工具会利用它，以检测编码错误，或者提供自动完成。比如， BarsArray 就是这样一个类型，我们可以用它来声明一个行情函数的返回值类型。它的特点时，以目前的 Python 版本（截止到 Python3.8) 来看，类型信息无法在运行时访问到。

另一类则是运行时类型，比如 FrameType 等。

#### FrameType
行情数据都是按帧进行封装的，比如，每 1 分钟为一个单位，封装了高开低收、成交量等信息。这样的单位常常还有 5 分钟，15 分钟，日线等等。 FrameType 列举了在 Zillionare 中常用的帧类型。在其它软件中，您可能看到`unit`或者`peroid`、周期等说法。当然，可能 FrameType 是最精准的一个词。

Zillionare 提供了以下对应帧类型：

| 周期      | 字符串 | 类型              | 数值 |
| --------- | ------ | ----------------- | ---- |
| 年线      | 1Y     | FrameType.YEAR    | 10   |
| 季线      | 1Q     | FrameType.QUARTER | 9    |
| 月线      | 1M     | FrameType.MONTH   | 8    |
| 周线      | 1W     | FrameType.WEEK    | 7    |
| 日线      | 1D     | FrameType.DAY     | 6    |
| 60 分钟线 | 60m    | FrameType.MIN60   | 5    |
| 30 分钟线 | 30m    | FrameType.MIN30   | 4    |
| 15 分钟线 | 15m    | FrameType.MIN15   | 3    |
| 5 分钟线  | 5m     | FrameType.MIN5    | 2    |
| 分钟线    | 1m     | FrameType.MIN1    | 1    |


FrameType还提供了 `<`, `<=`, `>=`, `>`等比较运算。

#### SecurityType
常见的证券交易品种定义。

| 类型                 | 值           | 说明      |
| -------------------- | ------------ | --------- |
| SecurityType.STOCK   | stock        | 股票类型  |
| SecurityType.INDEX   | index        | 指数类型  |
| SecurityType.ETF     | etf          | ETF基金   |
| SecurityType.FUND    | fund         | 基金      |
| SecurityType.LOF     | lof，LOF基金 |           |
| SecurityType.FJA     | fja          | 分级A基金 |
| SecurityType.FJB     | fjb          | 分级B基金 |
| SecurityType.BOND    | bond         | 债券基金  |
| SecurityType.STOCK_B | stock_b      | B股       |
| SecurityType.UNKNOWN | unknown      | 未知品种  |

它的一个用法是，在我们查询证券列表中，有哪些股票类型的代码时：

```python
secs = await Security.select().types(SecurityType.STOCK).eval()
print(secs)
```

#### MarketType

市场类型。Zillionare支持的类型为上交所`XSHG`和`XSHE`

| 类型            | 值   | 说明   |
| --------------- | ---- | ------ |
| MarketType.XSHG | XSHG | 上交所 |
| MarketType.XSHE | XSHE | 深交所 |

#### bars_dtype
在zillionare中，我们一般使用 Numpy Structured Array来存储行情数据，以使用numpy的许多性能算法进行运算。同时，它也比pandas.DataFrame更省内存，在小数据集（<50万条）时，多数运算（但不是每一种运算）会有更高的性能。

要使用 Numpy Structured Array来表示行情数据，就需要定义定段列表。 [bars_dtype](api/#coretypes.types.bars_dtype)就是这样的列表，它包括了字段（frame, open, high, low, close, volume, amount, factor)。

```python
bars_dtype = np.dtype(
    [
        ("frame", "datetime64[s]"),
        ("open", "f4"),
        ("high", "f4"),
        ("low", "f4"),
        ("close", "f4"),
        ("volume", "f8"),
        ("amount", "f8"),
        ("factor", "f4"),
    ]
)
```

#### bars_dtype_with_code

在 `bars_dtype`基础上增加了`code`字段，以用于同时存取多个证券的行情的情况。

```python
bars_dtype_with_code = np.dtype(
    [
        ("code", "O"),
        ("frame", "datetime64[s]"),
        ("open", "f4"),
        ("high", "f4"),
        ("low", "f4"),
        ("close", "f4"),
        ("volume", "f8"),
        ("amount", "f8"),
        ("factor", "f4"),
    ]
)
```

#### bars_cols、bars_with_limit_dtype, bars_with_limit_cols

即定义在`bars_dtype`中的字段列表。有时候我们需要在numpy与pandas dataframe之间进行转换时，往往需要这个变量的值。

`bars_with_limit_dtype`提供了带涨跌停报价的行情数据类型。

`bars_with_limit_cols`提供了定义在`bars_with_limit_dtype`中的字段名列表。

#### BarsArray
可用此静态类型作为行情数据（常用变量名 `bars`)的type hint，对应于`bars_dtype`。

#### BarsWithLimitArray
同`BarsArray`，但带涨跌停报价，对应于`bars_with_limit_array`。

#### BarsPanel
对应于`bars_dtype_with_code`的type hint类型。

#### xrxd_info_dtype
除权除息信息类型

#### security_info_dtype
定义了证券列表的字段

### Trade Errors

在coretypes.errors.trade中，定义了交易中常常可能出现的异常类型。在TradeClient, TraderServer和Backtesting Server间常常都需要使用它。

我们把Trade Errors分为客户端错误 `coretypes.errors.trade.client.*`, `coretypes.errors.trade.server.*`, `coretypes.errors.trade.entrust.*`三种类型，分别表明客户端编码、传参错误；服务器内部错误和交易类型错误。

!!! Tips
    对开发者而言，如果需要将此类异常传入到客户端，需要通过 [TraderError.as_json](api/#coretypes.errors.trade.base.TradeError.as_json)将其串行化后再通过网络发送，在客户端则可以通过[TraderError.from_json](api/#coretypes.errors.trade.base.TradeError.from_json)将其恢复。

    为方便查错，服务器还可以将调用栈通过`stack`参数传递给客户端。

### QuotesFetcher

Zillionare目前只适配了聚宽的数据源，但我们通过 QuotesFetcher 让您可以自行适配其它数据源。

你需要实现定义在 [QuotesFetcher](/api/#coretypes.quote_fetcher.QuotesFetcher)中的接口，然后在omega的配置文件中，加载您的实现。

具体实现可以参考 [omega-jqadaptor](https://github.com/zillionare/omega_jqadaptor)

配置可以参见[omega-config](https://github.com/zillionare/omega/blob/master/omega/config/defaults.yaml)

```yaml
# defaults.yaml

quotes_fetchers:
  - impl: jqadaptor    # there must be a create_instance method in this module
    account: ${JQ_ACCOUNT}
    password: ${JQ_PASSWORD}
```

## Credits

本项目使用[ppw](https://zillionare.github.io/python-project-wizard/)创建，并遵循ppw定义的代码风格和质量规范。
