# 🎯 松鼠AI 销售异议查询助手

> 一个 AI 驱动的销售异议知识库系统，帮助门店销售快速查询和应对客户异议。

## ✨ 核心特性

- 🔍 **智能搜索** - 快速找到相关异议
- 🤖 **AI 匹配** - 根据客户表述智能推荐异议
- 📚 **完整方案** - 每个异议配备 5-7 个回复方案 + 数据支撑 + 成功案例
- 📋 **一键复制** - 快速复制话术到销售工具
- 💼 **企业集成** - 支持钉钉、企业微信、CRM 集成
- 📊 **数据分析** - 统计最常见的异议和高评分方案
- 💾 **灵活导出** - 支持 Excel、JSON 等多种格式

## 📦 项目构成

```
├── objection_assistant.html      # 🎨 前端应用（直接打开即可用）
├── objection_assistant.py        # 🐍 数据管理系统（Python 后端）
├── api_server.py                 # 🚀 REST API 服务（企业集成）
├── requirements.txt              # 📋 依赖列表
├── 使用指南.md                   # 📖 完整使用说明
└── README.md                     # 📄 本文件
```

## 🚀 快速开始

### 方式1️⃣：网页版（推荐给销售）

最简单的方式 - 直接打开 HTML 文件：

```bash
# 1. 打开浏览器
open objection_assistant.html

# 2. 或者启动一个简单的 HTTP 服务器
python -m http.server 8000

# 3. 然后访问 http://localhost:8000/objection_assistant.html
```

✅ 优点：
- 无需安装任何依赖
- 可离线使用
- 支持所有现代浏览器
- 适合移动设备

### 方式2️⃣：Python 后端（数据管理）

用于管理异议库和导出数据：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行示例
python objection_assistant.py

# 3. 或在 Python 中使用
from objection_assistant import ObjectionAssistant

assistant = ObjectionAssistant()
results = assistant.search_objections("价格")
```

### 方式3️⃣：REST API 服务（企业集成）

部署为 API 服务，集成到企业系统：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 API 服务
python api_server.py

# 3. 访问 API 文档
# http://localhost:5000/

# 4. 示例请求
curl http://localhost:5000/api/objections/search -X POST \
  -H "Content-Type: application/json" \
  -d '{"keyword": "价格"}'
```

## 📚 异议库内容

目前包含 **28+ 条异议**，分为 8 大类：

| 分类 | 异议数 | 示例 |
|------|--------|------|
| 💰 价格相关 | 3 | "价格太贵"、"需要试用" |
| 📈 产品效果 | 2 | "效果不明显" |
| 🏆 竞争对比 | 2 | "竞品更好"、"已有线下班" |
| 👨‍👧 用户体验 | 1 | "孩子不愿意用" |
| ⏰ 时间相关 | 1 | "没有时间" |
| 🔒 信任相关 | 1 | "数据安全问题" |
| 🎯 决策流程 | 1 | "需要试用后再决定" |
| 🌟 品牌选择 | 1 | "为什么选你们" |

每个异议都包含：
- ❓ 异议描述
- 💡 问题分析  
- 🎯 3-5 个回复方案
- 📊 数据支撑点
- ✅ 成功案例
- 💬 销售技巧

## 🔍 功能演示

### 搜索异议

```bash
# Web 界面
- 在搜索框输入 "价格" 或 "贵"
- 系统自动匹配相关异议

# API 调用
curl -X POST http://localhost:5000/api/objections/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "价格"}'
```

### AI 智能匹配

```bash
curl -X POST http://localhost:5000/api/objections/match \
  -H "Content-Type: application/json" \
  -d '{"input": "你们的产品和竞品差不多，为什么我要选你们？"}'

# 系统自动推荐 Top 3 相关异议
```

### 获取统计

```bash
curl http://localhost:5000/api/statistics

# 输出：总异议数、分类数、总查询次数、平均评分等
```

### 导出数据

```bash
# Python 脚本
from objection_assistant import ObjectionAssistant
assistant = ObjectionAssistant()
assistant.export_to_excel("异议库.xlsx")
assistant.export_to_json("异议库.json")

# API 接口
curl http://localhost:5000/api/export/excel
curl http://localhost:5000/api/export/json
```

## 💻 API 文档

### 查询接口

```
GET    /api/objections              # 获取所有异议
GET    /api/objections/<id>         # 获取单个异议
POST   /api/objections/search       # 搜索异议（请求体：{"keyword": "关键词"}）
POST   /api/objections/match        # AI 匹配（请求体：{"input": "客户表述"}）
GET    /api/categories              # 获取所有分类
GET    /api/objections/category     # 按分类查询（查询参数：?name=分类名）
```

### 管理接口

```
POST   /api/objections              # 创建异议
PUT    /api/objections/<id>         # 更新异议
DELETE /api/objections/<id>         # 删除异议
POST   /api/objections/<id>/rate    # 评分异议
```

### 统计和导出

```
GET    /api/statistics              # 获取统计数据
GET    /api/statistics/usage        # 获取使用统计
GET    /api/export/excel            # 导出 Excel
GET    /api/export/json             # 导出 JSON
```

## 📖 使用场景

### 场景1：销售实时查询异议

```
1. 打开网页版 objection_assistant.html
2. 搜索关键词（如 "价格"）
3. 查看完整的回复方案
4. 复制话术进行销售
```

### 场景2：团队共享异议库

```
1. 部署 API 服务到公司服务器
2. 通过钉钉/企业微信分享访问链接
3. 所有销售可在线查询和反馈
```

### 场景3：CRM 系统集成

```
1. 在 CRM 系统中集成 API
2. 销售在 CRM 中直接查询异议
3. 自动记录查询历史和转化率
```

### 场景4：数据分析和优化

```
1. 定期导出数据到 Excel
2. 分析最常见的异议
3. 优化回复方案
4. 持续更新异议库
```

## 🔧 配置和部署

### 本地开发

```bash
# 1. 克隆项目
git clone <repo-url>
cd squirrel-objection-assistant

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动开发服务
python api_server.py

# 4. 打开浏览器
open http://localhost:5000
```

### 生产部署（Linux/Docker）

```bash
# 使用 Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app

# 或使用 Docker
docker build -t squirrel-objection .
docker run -p 5000:5000 squirrel-objection
```

### 企业集成

**钉钉集成：**
- 在钉钉工作台添加应用
- 链接到 `objection_assistant.html` 或 API 地址

**企业微信集成：**
- 创建应用
- 配置应用链接

**CRM 集成：**
- 使用 REST API
- 集成查询和反馈功能

## 📊 数据结构

### 异议对象

```json
{
  "id": 1,
  "title": "价格太贵，竞品更便宜",
  "category": "价格相关",
  "keywords": ["价格", "贵", "便宜"],
  "description": "客户认为产品价格过高",
  "analysis": "反映客户对产品价值认知不足",
  "solutions": ["方案1", "方案2", "方案3"],
  "dataPoints": ["数据点1", "数据点2"],
  "counterExamples": ["案例1", "案例2"],
  "tips": ["技巧1", "技巧2"],
  "createdAt": "2026-03-31T15:55:00",
  "updatedAt": "2026-03-31T15:55:00",
  "usageCount": 42,
  "rating": 4.8
}
```

## 🛠 开发和定制

### 添加新异议

```python
from objection_assistant import ObjectionAssistant

assistant = ObjectionAssistant()

new_objection = {
    'title': '新的异议',
    'category': '分类',
    'keywords': ['关键词1', '关键词2'],
    'description': '异议描述',
    'analysis': '问题分析',
    'solutions': ['方案1', '方案2'],
    'dataPoints': ['数据1'],
    'counterExamples': ['案例1'],
    'tips': ['技巧1']
}

result = assistant.add_objection(new_objection)
print(f"新异议已添加，ID: {result['id']}")
```

### 自定义 Web 界面

修改 `objection_assistant.html` 中的：
- `objectionsData` - 异议内容
- CSS 样式 - UI 主题
- JavaScript 逻辑 - 交互行为

### 扩展 API

在 `api_server.py` 中添加新的路由：

```python
@app.route('/api/custom-endpoint', methods=['POST'])
def custom_endpoint():
    # 自定义逻辑
    return jsonify({'status': 'success'})
```

## 📋 依赖

```
Flask==2.3.0
flask-cors==4.0.0
openpyxl==3.1.0
```

详见 `requirements.txt`

## ✅ 功能清单

- [x] 异议查询和搜索
- [x] AI 智能匹配
- [x] 完整回复方案库
- [x] 一键复制话术
- [x] 数据统计分析
- [x] Excel/JSON 导出
- [x] REST API 服务
- [x] 前端 Web 应用
- [x] Python 数据管理
- [ ] 微信小程序版
- [ ] 移动应用版
- [ ] 团队协作功能

## 🤝 贡献

欢迎提交反馈和改进建议！

1. 收集销售的实际异议
2. 优化现有的回复方案
3. 添加新的成功案例
4. 改进 UI/UX

## 📞 技术支持

遇到问题？

- 📖 查看 [完整使用指南](./使用指南.md)
- 📧 联系技术支持：support@example.com
- 🐛 提交 Bug 报告

## 📝 更新日志

### v1.0.0 (2026-03-31)
- ✨ 初版发布
- 📚 包含 28+ 条异议
- 🔍 智能搜索和 AI 匹配
- 📋 完整的 Web + API + Python 三层架构

## 📄 许可证

Copyright © 2026 Squirrel AI  
All rights reserved.

---

**快速开始：** `open objection_assistant.html` 即可使用！

**需要更多帮助？** 查看 [使用指南.md](./使用指南.md)
