# History

## 0.5.1 (2022-08-08)
* 修复了找到到mike[doc]安装包的错误。
## 0.5. （2022-08-06）

### breaking changes
* bars_dtype等类型中的frame字段的数据类型，由Object改为np.datetime64[s]，这个修改将有利于更快进行解析。

### Features

* 增加了BarsArray, BarsPanel和BarsWithLimitArray数据类型
* security_db_dtype, security_info_dtype, xrxd_info_dtype

## 0.1.0 (2022-01-12)

* First release on PyPI.
