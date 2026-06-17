# 包钢产销数据管理平台

基于 Flask + Doris 的 Web 应用，提供产品档案管理、自定义新产品、产销数据统计等功能。

## 快速开始

```bash
pip install -r requirements.txt
python run.py
```

访问: http://localhost:5000

## 配置

修改 `backend/config.py` 中的 `DORIS_CONFIG`:

```python
DORIS_CONFIG = {
    'host': '数据库地址',
    'port': 9030,
    'user': '用户名',
    'password': '密码',
    'database': '数据库名',
}
```

## 页面路由

| 路由 | 页面文件 | 说明 |
|------|----------|------|
| `/` | index.html | 主页 - 通用SQL查询工具（支持导出Excel） |
| `/product` | product.html | 产品基本信息档案（支持筛选、分页、导出Excel） |
| `/custom-product` | custom_product.html | 自定义新产品（支持新增/同步/删除、导出Excel） |
| `/production-sales` | production_sales.html | 产销数据统计（动态查询、数据校验、导出Excel） |

---

## API 接口文档

### 一、通用数据操作接口

#### 1. 查询数据

- **URL**: `/api/select`
- **方法**: `POST`
- **请求体**:
```json
{
  "table": "表名（必填）",
  "columns": ["col1", "col2"],  // 可选，默认 ["*"]
  "where": "条件表达式",          // 可选
  "limit": 100                   // 可选
}
```
- **成功响应**:
```json
{ "success": true, "data": [...], "sql": "SELECT ..." }
```
- **失败响应**:
```json
{ "success": false, "error": "错误信息", "sql": "SELECT ..." }
```

#### 2. 插入数据

- **URL**: `/api/insert`
- **方法**: `POST`
- **请求体**:
```json
{
  "table": "表名（必填）",
  "data": { "col1": "val1", "col2": "val2" }  // 必填
}
```
- **成功响应**:
```json
{ "success": true, "affected": 1, "sql": "INSERT ..." }
```

#### 3. 更新数据

- **URL**: `/api/update`
- **方法**: `POST`
- **请求体**:
```json
{
  "table": "表名（必填）",
  "data": { "col1": "new_val" },  // 必填
  "where": "id=1"                  // 必填
}
```
- **成功响应**:
```json
{ "success": true, "affected": 1, "sql": "UPDATE ..." }
```

#### 4. 删除数据

- **URL**: `/api/delete`
- **方法**: `POST`
- **请求体**:
```json
{
  "table": "表名（必填）",
  "where": "id=1"  // 必填
}
```
- **成功响应**:
```json
{ "success": true, "affected": 1, "sql": "DELETE ..." }
```

#### 5. 执行原始SQL

- **URL**: `/api/sql`
- **方法**: `POST`
- **请求体**:
```json
{ "sql": "SHOW DATABASES" }
```
- **成功响应（查询类）**:
```json
{ "success": true, "data": [...], "sql": "SHOW DATABASES" }
```
- **成功响应（修改类）**:
```json
{ "success": true, "affected": 1, "sql": "..." }
```

---

### 二、产品基本信息档案接口

> 操作表: `tmp_analysis.mid_product_base_info_d_f`

#### 6. 获取产品筛选选项

- **URL**: `/api/product/filters`
- **方法**: `GET`
- **请求参数**: 无
- **响应**:
```json
{
  "success": true,
  "options": {
    "prodclass": ["01", "02", ...],
    "prodclasschin": ["板材", "线材", ...],
    "prodtype": ["A", "B", ...],
    "prodtypechin": ["热轧", "冷轧", ...]
  }
}
```

#### 7. 查询产品列表

- **URL**: `/api/product/list`
- **方法**: `POST`
- **请求体**:
```json
{
  "prodclass": "产品大类编码（可选）",
  "prodclasschin": "产品大类名称（可选）",
  "prodtype": "产品形态编码（可选）",
  "prodtypechin": "产品形态名称（可选）",
  "page": 1,
  "pageSize": 50
}
```
- **响应**:
```json
{
  "success": true,
  "data": [...],
  "total": 100,
  "page": 1,
  "pageSize": 50
}
```

---

### 三、自定义新产品接口

> 操作表: `tmp_analysis.mid_custom_new_product_info`

#### 8. 获取自定义产品表单选项

- **URL**: `/api/custom-product/options`
- **方法**: `GET`
- **请求参数**: 无
- **响应**:
```json
{
  "success": true,
  "options": {
    "prodclass": [...],
    "prodclasschin": [...],
    "prodtype": [...],
    "prodtypechin": [...],
    "mscno": [...],
    "apnno": [...],
    "apndesc": [...],
    "custom_mark": ["虚拟产品", "新增实际产品"]
  }
}
```
- **说明**: 选项数据从产品基本信息底表 (`mid_product_base_info_d_f`) 获取，`custom_mark` 为固定选项。

#### 9. 新增自定义产品

- **URL**: `/api/custom-product/add`
- **方法**: `POST`
- **请求体**:
```json
{
  "psrno": "产品规范编码（必填）",
  "prodclass": "产品大类编码（可选）",
  "prodclasschin": "产品大类中文名称（可选）",
  "prodtype": "产品形态编码（可选）",
  "prodtypechin": "产品形态中文名称（可选）",
  "mscno": "制造标准编码（可选）",
  "apnno": "用途码（可选）",
  "apndesc": "用途中文描述（可选）",
  "standname": "标准全名（可选）",
  "custom_mark": "自定义产品标记（可选）"
}
```
- **自动填充字段**: `create_time` = `NOW()`, `source_from` = `'人工定义'`
- **成功响应**:
```json
{ "success": true, "affected": 1, "sql": "INSERT ..." }
```

#### 10. 查询自定义产品列表

- **URL**: `/api/custom-product/list`
- **方法**: `POST`
- **请求体**:
```json
{
  "psrno": "产品规范编码（可选）",
  "prodclass": "产品大类编码（可选）",
  "prodclasschin": "产品大类名称（可选）",
  "prodtype": "产品形态编码（可选）",
  "prodtypechin": "产品形态名称（可选）",
  "custom_mark": "自定义产品标记（可选）",
  "page": 1,
  "pageSize": 50
}
```
- **响应**:
```json
{
  "success": true,
  "data": [...],
  "total": 10,
  "page": 1,
  "pageSize": 50
}
```
- **排序**: 按 `create_time DESC` 降序

#### 11. 同步自定义产品到产品基本信息底表

- **URL**: `/api/custom-product/sync`
- **方法**: `POST`
- **请求体**:
```json
{ "psrno": "产品规范编码（必填）" }
```
- **处理逻辑**:
  1. 从 `mid_custom_new_product_info` 查询该 psrno 的记录
  2. 检查 `mid_product_base_info_d_f` 是否已存在该 psrno
  3. **已存在** → UPDATE 更新匹配字段
  4. **不存在** → INSERT 插入新记录
- **同步字段映射** (`CUSTOM_PRODUCT_SYNC_MAP`):

| 自定义表字段 | 底表字段 | 说明 |
|-------------|---------|------|
| prodclass | prodclass | 产品大类编码 |
| prodclasschin | prodclasschin | 产品大类中文名称 |
| prodtype | prodtype | 产品形态编码 |
| prodtypechin | prodtypechin | 产品形态中文名称 |
| mscno | mscno | 制造标准编码 |
| apnno | apnno | 用途码 |
| apndesc | apndesc | 用途中文描述 |

- **成功响应**:
```json
{ "success": true, "action": "更新|插入", "affected": 1, "sql": "...", "psrno": "xxx" }
```

#### 12. 删除自定义产品

- **URL**: `/api/custom-product/delete`
- **方法**: `POST`
- **请求体**:
```json
{ "psrno": "产品规范编码（必填）" }
```
- **成功响应**:
```json
{ "success": true, "affected": 1, "psrno": "xxx" }
```
- **记录不存在**: 返回 404
```json
{ "success": false, "error": "未找到psrno=xxx的记录" }
```

#### 13. 获取虚拟产品配置

- **URL**: `/api/custom-product/virtual`
- **方法**: `GET`
- **请求参数**: `?psrno=xxx`
- **说明**: 根据 psrno 从自定义产品表中查找 `custom_mark='虚拟产品'` 的记录，按映射关系转换为产销统计的筛选条件和分组维度。
- **虚拟产品字段映射** (`VIRTUAL_PRODUCT_FILTER_MAP`):

| 自定义表字段 | 产销统计维度 | 说明 |
|-------------|-------------|------|
| prodclass | prodClass | 产品大类 |
| prodtype | prodCode | 产品代码 |
| apnno | apnno | 用途码 |

- **响应**:
```json
{
  "success": true,
  "psrno": "xxx",
  "filters": { "prodClass": "值", "prodCode": "值", "apnno": "值" },
  "groupBy": ["prodClass", "prodCode", "apnno"],
  "rawRecord": { ... }
}
```
- **说明**: `filters` 中只包含有值的字段，`groupBy` 与 `filters` 的 key 一致；无值的字段不出现在结果中，表示用户不以此字段作为筛选或分组条件。

---

### 四、产销数据统计接口

> 操作表: `bg_isale.pending_settlement_ss10`（待结算）+ `bg_isale.settlement_ss15`（已结算）

#### 14. 获取产销统计筛选选项

- **URL**: `/api/production-sales/options`
- **方法**: `GET`
- **请求参数**: 无
- **说明**: 从待结算和已结算两张表 UNION 查询各维度的 DISTINCT 值。
- **响应**:
```json
{
  "success": true,
  "options": {
    "factory": ["制造厂1", ...],
    "oemVenCode": ["委托加工厂1", ...],
    "subFactoryNo": ["二级厂矿1", ...],
    "factoryLine": ["生产线1", ...],
    "contChannel": ["渠道1", ...],
    "prodCode": ["产品代码1", ...],
    "prodClass": ["产品大类1", ...],
    "tradeNo": ["钢种1", ...],
    "psrNo": ["规范代码1", ...],
    "apnno": ["用途码1", ...],
    "settle_status": ["待结算", "已结算"]
  },
  "dimensions": [["stat_month", "统计月份", "date_range"], ...],
  "metrics": [["order_count", "订单总数"], ...]
}
```

#### 15. 执行产销统计查询

- **URL**: `/api/production-sales/query`
- **方法**: `POST`
- **请求体**:
```json
{
  "filters": {
    "factory": "制造厂（可选）",
    "prodClass": "产品大类（可选）",
    "settle_status": "待结算|已结算（可选）",
    "specMark": "规格关键词（可选，模糊匹配）",
    "...": "其他维度（可选）"
  },
  "groupBy": ["stat_period", "factory", "settle_status"],
  "timeGranularity": "month",
  "dateStart": "2026-01-01",
  "dateEnd": "2026-06-30",
  "page": 1,
  "pageSize": 50
}
```
- **必填**: `dateStart`, `dateEnd`, `groupBy`（至少一个维度）
- **timeGranularity 可选值**:

| 值 | 说明 | SQL表达式 | 列名 |
|----|------|----------|------|
| `year` | 按年聚合 | `DATE_FORMAT(shipDate, '%Y')` | 统计年份 |
| `quarter` | 按季度聚合 | `CONCAT(DATE_FORMAT(shipDate, '%Y'), '-Q', QUARTER(shipDate))` | 统计季度 |
| `month` | 按月聚合（默认） | `DATE_FORMAT(shipDate, '%Y-%m')` | 统计月份 |
| `week` | 按周聚合 | `CONCAT(DATE_FORMAT(shipDate, '%Y'), '-W', WEEK(shipDate))` | 统计周 |
| `day` | 按日聚合 | `DATE_FORMAT(shipDate, '%Y-%m-%d')` | 统计日期 |

- **SQL构建逻辑**:
  1. 基础子查询: UNION ALL 合并待结算（标记`'待结算'`）和已结算（标记`'已结算'`）两张表
  2. SELECT: 用户勾选的分组维度（中文别名）+ 21个聚合指标；当 `stat_period` 在 groupBy 中时，根据 `timeGranularity` 选择对应的时间表达式
  3. WHERE: `shipDate BETWEEN ... AND ...` + 用户填写的筛选条件
  4. GROUP BY: 用户勾选的维度（`stat_period` 使用对应的时间表达式）
  5. ORDER BY: 时间维度 ASC, settle_status DESC（如果对应维度在分组中）
- **响应**:
```json
{
  "success": true,
  "data": [...],
  "total": 100,
  "page": 1,
  "pageSize": 50,
  "sql": "SELECT ...",
  "dimensionLabels": ["统计月份", "制造厂"],
  "metricLabels": ["订单总数", "总出货数量", "..."]
}
```
- **说明**: `dimensionLabels` 为维度列显示名（与groupBy对应），`metricLabels` 为指标列显示名，前端据此排列维度列在前、指标列在后。

---

#### 16. 数据校验（三层校验）

- **URL**: `/api/production-sales/validate`
- **方法**: `POST`
- **说明**: 比对系统统计结果与人工报数，执行三层校验：①总条数一致性 ②维度组合一致性（漏报/多报）③字段级校验（数值差异、遗漏字段、多报字段）
- **请求体**:
```json
{
  "systemData": [{"统计月份": "2026-01", "制造厂": "xxx", "订单总数": 100, ...}],
  "manualData": [{"统计月份": "2026-01", "制造厂": "xxx", "订单总数": 98, ...}],
  "groupBy": ["stat_period", "factory"],
  "timeGranularity": "month",
  "threshold": 5
}
```
- **参数说明**:
  - `systemData`: 系统查询结果（前端传入，非后端重新查询）
  - `manualData`: 人工报数数据（前端上传文件或手动填写）
  - `groupBy`: 分组维度列表（用于确定维度列名）
  - `timeGranularity`: 时间聚合尺度（用于解析stat_period的显示名）
  - `threshold`: 差异阈值百分比，超过此值的字段标为差异（默认5）

- **响应**:
```json
{
  "success": true,
  "summary": {
    "totalSystem": 10,
    "totalManual": 9,
    "rowCountMatch": false,
    "matchedCombos": 8,
    "extraCombos": 1,
    "missCombos": 2,
    "commonColumns": ["统计月份", "制造厂", "订单总数"],
    "missingInManual": ["总出货重量"],
    "extraInManual": ["备注"]
  },
  "details": [
    {
      "rowStatus": "matched|extra|miss",
      "manualRow": {...},
      "systemRow": {...},
      "fieldChecks": {
        "订单总数": {
          "status": "match|diff|missing_in_manual|extra_in_manual",
          "manualVal": 98,
          "systemVal": 100,
          "diff": -2,
          "diffRate": -2.0
        }
      }
    }
  ],
  "dimensionColumns": ["统计月份", "制造厂"],
  "matchDimensions": ["统计月份", "制造厂"]
}
```

- **三层校验逻辑**:
  1. **总条数校验**: 比较 `len(systemData)` 与 `len(manualData)`
  2. **维度组合校验**: 取共有维度列构建组合键，匹配/多报/漏报
  3. **字段级校验**: 对匹配条目逐字段比对，数值型计算差异率和差异值，非数值型比对一致性；标识人工遗漏字段和多报字段

---

#### 17. 统一导出Excel

- **URL**: `/api/export/excel`
- **方法**: `POST`
- **说明**: 统一Excel导出接口，支持多Sheet、表头样式、自动列宽。所有页面共用此接口导出数据。
- **请求体**:
```json
{
  "fileName": "导出文件名（不含扩展名）",
  "sheets": [
    {
      "sheetName": "Sheet1",
      "columns": ["列1", "列2", "..."],
      "data": [[val1, val2, "..."], ...]
    }
  ]
}
```
- **响应**: 返回 `.xlsx` 文件流（`Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`）
- **Excel样式**:
  - 表头：加粗 + 蓝色背景(`#D9E1F2`) + 居中 + 细边框
  - 数据：左对齐 + 细边框
  - 列宽：根据内容自动调整（中文字符按2倍宽度计算，最大50）

- **各页面导出说明**:

| 页面 | 导出按钮 | 数据来源 | 说明 |
|------|---------|---------|------|
| 主页(index) | 导出Excel | 当前SQL查询结果 | 无分页，直接导出 |
| 产品档案(product) | 导出Excel | 重新请求全量数据(pageSize=999999) | 保持当前筛选条件 |
| 自定义产品(custom_product) | 导出Excel | 重新请求全量数据(pageSize=999999) | — |
| 产销统计(production_sales) | 导出查询结果 | 重新请求全量数据(pageSize=999999) | 保持筛选/分组/时间条件 |
| 产销统计(production_sales) | 导出校验结果 | 前端校验结果数据 | 双Sheet：校验汇总+字段级详情 |

---

### 五、健康检查

#### 18. 健康检查

- **URL**: `/api/health`
- **方法**: `GET`
- **成功响应**:
```json
{ "status": "healthy", "database": "connected" }
```
- **失败响应** (500):
```json
{ "status": "unhealthy", "database": "disconnected" }
```

---

## 常量与配置说明

### 数据库表

| 常量名 | 值 | 说明 |
|--------|-----|------|
| `PRODUCT_TABLE` | `tmp_analysis.mid_product_base_info_d_f` | 产品基本信息底表 |
| `CUSTOM_PRODUCT_TABLE` | `tmp_analysis.mid_custom_new_product_info` | 自定义新产品表 |
| `PENDING_TABLE` | `bg_isale.pending_settlement_ss10` | 待结算数据表 |
| `SETTLED_TABLE` | `bg_isale.settlement_ss15` | 已结算数据表 |

### 产品筛选字段 (`FILTER_FIELDS`)

| 前端参数名 | 数据库列名 | 显示名称 |
|-----------|-----------|---------|
| prodclass | prodclass | 产品大类编码 |
| prodclasschin | prodclasschin | 产品大类名称 |
| prodtype | prodtype | 产品形态编码 |
| prodtypechin | prodtypechin | 产品形态名称 |

### 自定义产品字段 (`CUSTOM_PRODUCT_FIELDS`)

| 数据库列名 | 显示名称 | 从底表取选项 |
|-----------|---------|------------|
| psrno | 产品规范编码 | 否 |
| prodclass | 产品大类编码 | 是 |
| prodclasschin | 产品大类中文名称 | 是 |
| prodtype | 产品形态编码 | 是 |
| prodtypechin | 产品形态中文名称 | 是 |
| mscno | 制造标准编码 | 是 |
| apnno | 用途码 | 是 |
| apndesc | 用途中文描述 | 是 |
| standname | 标准全名 | 否 |
| custom_mark | 自定义产品标记 | 否（固定选项） |

### 产销统计维度 (`PS_DIMENSIONS`)

| 数据库列名 | 显示名称 | 筛选类型 |
|-----------|---------|---------|
| stat_period | 时间维度 | time_period（支持年/季度/月/周/日聚合） |
| factory | 制造厂 | select |
| oemVenCode | 委托加工厂 | select |
| subFactoryNo | 钢联二级厂矿 | select |
| factoryLine | 生产线 | select |
| contChannel | 销售渠道 | select |
| prodCode | 产品代码 | select |
| prodClass | 产品大类 | select |
| tradeNo | 钢筋钢种_材质 | select |
| psrNo | 产品规范代码 | select |
| specMark | 产品规格描述 | text（模糊匹配） |
| apnno | 用途码 | select |
| settle_status | 结算状态 | fixed（待结算/已结算） |

### 产销统计指标 (`PS_METRICS`)

| 指标key | SQL表达式 | 显示名称 |
|---------|----------|---------|
| order_count | COUNT(DISTINCT orderNo) | 订单总数 |
| order_item_count | COUNT(DISTINCT CONCAT(orderNo, orderItem)) | 订单项次总数 |
| total_deli_qty | SUM(deliQty) | 总出货数量 |
| total_deli_wet | SUM(deliWet) | 总出货重量 |
| total_pack_wet | SUM(packWet) | 总包装重量 |
| total_discount_qty | SUM(discountQty) | 总折让数量 |
| total_discount_wet | SUM(discountWet) | 总折让重量 |
| total_tai_amt | SUM(taiAmt) | 台币货款总金额 |
| total_frn_amt | SUM(frnAmt) | 外币货款总金额 |
| total_tax_amt | SUM(taxAmt) | 总税额 |
| total_adv_charge | SUM(advCharge) | 总订金金额 |
| total_interest_amt | SUM(interestAmt) | 总付款附价 |
| total_discount_amt | SUM(discountAmt) | 总现金折扣未税 |
| total_trans_cost | SUM(transCost) | 总运费 |
| total_pack_fee | SUM(packFee) | 总捆绑费 |
| total_port_cost | SUM(portCost) | 总站港杂费 |
| total_insurance | SUM(insurance) | 总SS保费 |
| total_agent_trans_cost | SUM(agentTransCost) | 代收代付运费总额 |
| total_car_price_amount | SUM(carPriceAmount) | 自备车租金总额 |
| total_shipping_costs | SUM(shippingcosts) | 预估海运费总额 |
| total_commission | SUM(commission) | 预估佣金总额 |

### 字段映射关系

**时间聚合尺度** (`TIME_GRANULARITY_MAP`):

| 尺度key | SQL表达式 | 显示名称 |
|---------|----------|---------|
| year | `DATE_FORMAT(shipDate, '%Y')` | 统计年份 |
| quarter | `CONCAT(DATE_FORMAT(shipDate, '%Y'), '-Q', QUARTER(shipDate))` | 统计季度 |
| month | `DATE_FORMAT(shipDate, '%Y-%m')` | 统计月份 |
| week | `CONCAT(DATE_FORMAT(shipDate, '%Y'), '-W', WEEK(shipDate))` | 统计周 |
| day | `DATE_FORMAT(shipDate, '%Y-%m-%d')` | 统计日期 |

**同步映射** (`CUSTOM_PRODUCT_SYNC_MAP`) — 自定义产品同步到底表:

| 自定义表字段 | 底表字段 |
|-------------|---------|
| prodclass | prodclass |
| prodclasschin | prodclasschin |
| prodtype | prodtype |
| prodtypechin | prodtypechin |
| mscno | mscno |
| apnno | apnno |
| apndesc | apndesc |

**虚拟产品映射** (`VIRTUAL_PRODUCT_FILTER_MAP`) — 虚拟产品导入产销统计:

| 自定义表字段 | 产销统计维度 |
|-------------|-------------|
| prodclass | prodClass |
| prodtype | prodCode |
| apnno | apnno |

---

## 项目结构

```
├── backend/
│   ├── app.py          # Flask主应用，所有API接口
│   ├── config.py       # Doris连接配置和Flask配置
│   └── db.py           # Doris数据库连接器（pymysql）
├── front/
│   ├── index.html              # 主页 - 通用SQL工具
│   ├── product.html            # 产品基本信息档案
│   ├── custom_product.html     # 自定义新产品
│   └── production_sales.html   # 产销数据统计
├── run.py              # 启动入口
├── start.bat           # Windows启动脚本
└── requirements.txt    # Python依赖
```

---

## 产销数据可视化

### 一、功能概述

用户在产销统计页面动态配置筛选条件和分组维度后，点击"一键可视化"按钮，系统自动根据当前查询条件生成6张业务图表，直观呈现产销数据的趋势、结构、量价关系和费用分布。

### 二、与其他接口的协作

可视化接口 `/api/production-sales/visualization` 与查询接口 `/api/production-sales/query` 共享完全相同的输入参数和SQL构建逻辑：

**输入来源**：前端从产销统计页面的筛选条件区域和分组维度勾选框中收集参数，与执行查询时使用的参数完全一致：

| 参数 | 来源 | 说明 |
|------|------|------|
| `filters` | 筛选条件下拉框/文本框 | 制造厂、产品大类、结算状态等 |
| `groupBy` | 分组维度勾选框 | 用户勾选的维度列表 |
| `timeGranularity` | 时间聚合尺度下拉框 | 年/季度/月/周/日 |
| `dateStart` / `dateEnd` | 日期选择器 | 发货日期范围 |

**与查询接口的区别**：可视化接口不分页（获取全量聚合数据），返回的是ECharts图表配置而非表格数据。

**协作流程**：
1. 用户在页面配置筛选条件、分组维度、时间范围
2. 点击"一键可视化"按钮
3. 前端收集与查询接口相同的参数，POST到 `/api/production-sales/visualization`
4. 后端构建与查询接口相同的SQL，获取全量聚合结果
5. 后端根据维度结构和指标含义，生成6张图表的ECharts配置
6. 前端接收配置后初始化ECharts实例并渲染

### 三、6张图表的设计思路

#### 图1：出货重量趋势

- **指标**：总出货重量
- **业务含义**：展示出货量随时间或分组维度的变化趋势
- **图表类型**：
  - 有时间维度 + 无分类维度 → 单系列折线图
  - 有时间维度 + 有分类维度 → 多系列折线图（每个分类一条线）
  - 无时间维度 → 柱状图
- **量纲问题**：单指标，无量纲冲突

#### 图2：货款金额趋势

- **指标**：台币货款总金额
- **业务含义**：展示货款金额随时间或分组维度的变化趋势
- **图表类型**：与图1相同的适配逻辑
- **量纲问题**：单指标，无量纲冲突

#### 图3：各组出货重量占比

- **指标**：总出货重量
- **业务含义**：展示各分组维度下出货重量的占比结构
- **图表类型**：环形饼图
- **切片来源**：优先使用分类维度（如制造厂、产品大类），无分类维度时使用时间维度
- **防拥挤**：切片上限8个，超出部分合并为"其他"
- **量纲问题**：饼图展示百分比，天然消除量纲差异

#### 图4：出货量与货款额

- **指标**：总出货重量（柱）+ 台币货款总金额（线）
- **业务含义**：对比出货量与货款金额的联动关系，发现量价背离
- **图表类型**：双Y轴柱线混合图（左Y轴=重量，右Y轴=金额）
- **量纲问题**：双Y轴分离，重量和金额各自独立刻度

#### 图5：订单数与货款额

- **指标**：订单总数（柱）+ 台币货款总金额（线）
- **业务含义**：对比订单数量与货款金额的关系，反映订单单价——同样货款额下订单越少，单价越高
- **图表类型**：双Y轴柱线混合图（左Y轴=订单数，右Y轴=货款金额）
- **适配逻辑**：与图4结构相同
  - 有时间维度 + 无分类维度 → 单系列柱线
  - 有时间维度 + 有分类维度 → 多系列柱线（每个分类一组柱+线）
  - 无时间维度 → 单系列柱线（X轴为分类维度值）
- **量纲问题**：双Y轴分离，订单数和金额各自独立刻度

#### 图6：各项费用占比

- **指标**：总税额 + 总运费 + 总捆绑费 + 总站港杂费 + 总SS保费 + 代收代付运费总额 + 自备车租金总额 + 预估海运费总额 + 预估佣金总额（共9项）
- **业务含义**：展示各项费用在总费用中的占比结构
- **图表类型**：环形饼图
- **量纲问题**：饼图展示百分比，消除费用项之间的量级差异（如运费百万级vs捆绑费千级）
- **特殊处理**：不过滤全零项，超10项合并为"其他"

### 四、后端构建图表信息的逻辑

后端接口的核心流程分为三步：

#### 步骤1：构建并执行SQL（复用查询接口逻辑）

```python
# 1. UNION ALL合并待结算和已结算表
base_query = f"SELECT ... FROM {PENDING_TABLE} UNION ALL SELECT ... FROM {SETTLED_TABLE}"

# 2. SELECT = 分组维度(中文别名) + 21个聚合指标
# 3. WHERE = 日期范围 + 用户筛选条件
# 4. GROUP BY = 用户勾选的维度
# 5. ORDER BY = 时间ASC, 结算状态DESC
# 6. 不分页，获取全量数据
```

#### 步骤2：分析维度结构

```python
has_time = 'stat_period' in group_by       # 是否有时间维度
cat_dims = [d for d in group_by if d != 'stat_period']  # 分类维度列表
has_settle = 'settle_status' in group_by   # 是否有结算状态维度
```

这三个布尔变量决定了每张图的适配方式：
- `has_time` → 图1/2用折线图还是柱状图，图4/5的X轴是时间还是分类
- `cat_dims` → 图1/2/4/5单系列还是多系列，图3/6的切片来源
- `has_settle` → 图3的切片是否包含结算状态分类

#### 步骤3：为每张图生成ECharts option

后端直接生成ECharts的`option` JSON对象，包含`tooltip`、`legend`、`xAxis`、`yAxis`、`series`等完整配置。关键辅助函数：

- `build_series(metric_label, chart_type)` — 根据指标名和图表类型构建series数据
  - 无分类维度：直接从result取值
  - 有分类维度：构建 `{dim_key: {time_val: value}}` 映射，按时间轴排列
- `safe_num(val)` — 安全转数值，处理NULL和异常值
- 系列数限制 `MAX_SERIES=12`，饼图切片限制8或10

返回格式：
```json
{
  "success": true,
  "charts": [
    { "chartType": "line", "title": "出货重量趋势", "option": { ... } },
    { "chartType": "pie", "title": "各组出货重量占比", "option": { ... } },
    ...
  ],
  "dataCount": 42
}
```

### 五、前端处理图表信息的流程

前端收到后端返回的`charts`数组后，按以下流程渲染：

#### 1. 销毁旧实例

```javascript
vizChartInstances.forEach(function(c) { c.dispose(); });
```

每次点击"一键可视化"前，先销毁所有已存在的ECharts实例，避免内存泄漏。

#### 2. 创建DOM容器

在2列网格布局中，为每张图创建一个容器div：

```html
<div class="viz-chart-item">
  <div class="viz-chart-title">出货重量趋势</div>
  <div class="viz-chart-container" id="viz_chart_0"></div>
</div>
```

所有图表等高380px，2列排列，形成3行2列的网格。

#### 3. 初始化ECharts并设置option

```javascript
const chartInstance = echarts.init(dom);
vizChartInstances.push(chartInstance);

// 补充通用样式
option.color = ['#667eea', '#52c41a', ...];  // 统一配色
option.toolbox = { feature: { saveAsImage, dataView } };  // 工具栏

chartInstance.setOption(option);
```

后端返回的`option`是完整的ECharts配置，前端只需补充配色和工具栏即可直接使用。

#### 4. 窗口自适应

```javascript
window.addEventListener('resize', function() {
    vizChartInstances.forEach(function(c) {
        if (c && !c.isDisposed()) c.resize();
    });
});
```

#### 5. 重置清理

点击"重置"按钮时，销毁所有ECharts实例并隐藏图表区域。

### 六、技术选型

| 组件 | 选型 | 说明 |
|------|------|------|
| 图表库 | ECharts 5.5.0 (CDN) | 功能全面，配置驱动，支持响应式 |
| 图表配置生成 | 后端Python | 根据维度结构智能适配，前端零逻辑 |
| 前后端数据格式 | ECharts option JSON | 后端直接生成可用的option，前端setOption即可 |