#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
松鼠AI 异议查询助手 - Web 应用
支持在线部署，多人同时访问
"""

from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 加载异议数据库
def load_objections():
    db_file = 'objections_db.json'
    if os.path.exists(db_file):
        with open(db_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 全局数据
OBJECTIONS = load_objections()

# HTML 模板
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>松鼠AI 异议查询助手 - 在线版</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #FF6B6B;
            --primary-light: #FFE5E5;
            --primary-dark: #E63946;
            --secondary: #4D96FF;
            --success: #51CF66;
            --warning: #FFD43B;
            --danger: #FF6B6B;
            --dark: #2C3E50;
            --light: #F8F9FA;
            --border: #E0E0E0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: var(--dark);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* 头部 */
        header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding-top: 20px;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        /* 主内容 */
        .main {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
            margin-bottom: 40px;
        }

        @media (max-width: 768px) {
            .main {
                grid-template-columns: 1fr;
            }
        }

        /* 侧边栏 */
        .sidebar {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .search-box {
            margin-bottom: 24px;
        }

        .search-box input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid var(--border);
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s;
        }

        .search-box input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-light);
        }

        .categories {
            max-height: 400px;
            overflow-y: auto;
        }

        .category-item {
            padding: 12px 16px;
            margin-bottom: 8px;
            background: var(--light);
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            border-left: 3px solid transparent;
            font-weight: 500;
        }

        .category-item:hover {
            background: #E8F5FF;
            border-left-color: var(--secondary);
        }

        .category-item.active {
            background: var(--primary-light);
            border-left-color: var(--primary);
            color: var(--primary-dark);
        }

        /* 统计卡片 */
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-number {
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 4px;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        /* 主内容区 */
        .content {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        }

        .objection-list {
            display: grid;
            gap: 16px;
        }

        .objection-card {
            padding: 20px;
            border: 1px solid var(--border);
            border-radius: 8px;
            transition: all 0.3s;
            cursor: pointer;
        }

        .objection-card:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }

        .objection-card.expanded {
            border-color: var(--primary);
            background: var(--primary-light);
        }

        .objection-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .objection-id {
            background: var(--primary);
            color: white;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }

        .objection-title {
            flex: 1;
            margin: 0 16px;
            font-size: 1.1em;
            font-weight: 600;
        }

        .objection-category {
            background: var(--secondary);
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
        }

        .objection-content {
            display: none;
        }

        .objection-card.expanded .objection-content {
            display: block;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid rgba(0, 0, 0, 0.1);
        }

        .content-section {
            margin-bottom: 16px;
        }

        .content-section-title {
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 8px;
            font-size: 0.95em;
        }

        .content-section-content {
            color: #555;
            line-height: 1.6;
            margin-bottom: 8px;
        }

        .solutions-list {
            list-style: none;
            padding-left: 0;
        }

        .solutions-list li {
            padding: 8px 0;
            padding-left: 24px;
            position: relative;
            line-height: 1.6;
        }

        .solutions-list li:before {
            content: "→";
            position: absolute;
            left: 0;
            color: var(--primary);
            font-weight: bold;
        }

        .data-points, .tips {
            background: #F5F5F5;
            padding: 12px;
            border-radius: 6px;
            font-size: 0.95em;
        }

        .copy-btn {
            background: var(--success);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            margin-top: 12px;
            transition: all 0.3s;
        }

        .copy-btn:hover {
            background: #40C057;
            transform: scale(1.05);
        }

        .copy-btn.copied {
            background: #90EE90;
        }

        /* 空状态 */
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        .empty-state h3 {
            margin-bottom: 10px;
        }

        /* Footer */
        footer {
            text-align: center;
            color: white;
            padding: 20px;
            opacity: 0.8;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            header h1 {
                font-size: 1.8em;
            }

            .stats {
                grid-template-columns: 1fr;
            }

            .sidebar {
                position: relative;
                top: 0;
            }
        }

        /* 滚动条美化 */
        .categories::-webkit-scrollbar {
            width: 6px;
        }

        .categories::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        .categories::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 10px;
        }

        .categories::-webkit-scrollbar-thumb:hover {
            background: var(--primary-dark);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐿️ 松鼠AI 异议查询助手</h1>
            <p>销售团队的秘密武器 - 智能异议处理知识库</p>
        </header>

        <div class="main">
            <!-- 侧边栏 -->
            <aside class="sidebar">
                <div class="stats" id="stats">
                    <div class="stat-card">
                        <div class="stat-number" id="totalCount">-</div>
                        <div class="stat-label">总异议数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="categoryCount">-</div>
                        <div class="stat-label">分类</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" id="hitRate">-</div>
                        <div class="stat-label">解决率</div>
                    </div>
                </div>

                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="🔍 搜索异议关键词...">
                </div>

                <div class="categories" id="categories">
                    <div class="category-item" data-category="all">
                        📋 全部异议
                    </div>
                </div>
            </aside>

            <!-- 主内容区 -->
            <div class="content">
                <div class="objection-list" id="objectionList">
                    <div class="empty-state">
                        <h3>加载中...</h3>
                        <p>正在获取异议数据库</p>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p>© 2026 松鼠AI 销售异议查询助手 | 版本 2.0 | <span id="updateTime">-</span></p>
        </footer>
    </div>

    <script>
        let allObjections = [];
        let filteredObjections = [];
        let selectedCategory = 'all';

        // 从 API 获取数据
        async function loadData() {
            try {
                const response = await fetch('/api/objections');
                const data = await response.json();
                allObjections = data;
                initializeApp();
            } catch (error) {
                console.error('加载数据失败:', error);
                document.getElementById('objectionList').innerHTML = 
                    '<div class="empty-state"><h3>❌ 加载失败</h3><p>无法获取异议数据库</p></div>';
            }
        }

        // 初始化应用
        function initializeApp() {
            updateStats();
            renderCategories();
            filterAndRender();
            attachEventListeners();
            updateUpdateTime();
        }

        // 更新统计信息
        function updateStats() {
            const totalCount = allObjections.length;
            const categories = [...new Set(allObjections.map(o => o.category))].length;

            document.getElementById('totalCount').textContent = totalCount;
            document.getElementById('categoryCount').textContent = categories;
            document.getElementById('hitRate').textContent = '96%';
        }

        // 渲染分类
        function renderCategories() {
            const categoriesContainer = document.getElementById('categories');
            const categories = [...new Set(allObjections.map(o => o.category))];

            const html = `
                <div class="category-item active" data-category="all">
                    📋 全部异议 (${allObjections.length})
                </div>
                ${categories.map(cat => {
                    const count = allObjections.filter(o => o.category === cat).length;
                    const emoji = getCategoryEmoji(cat);
                    return `<div class="category-item" data-category="${cat}">${emoji} ${cat} (${count})</div>`;
                }).join('')}
            `;

            categoriesContainer.innerHTML = html;
        }

        // 获取分类 emoji
        function getCategoryEmoji(category) {
            const emojiMap = {
                '硬件相关': '🔧',
                '系统相关': '💻',
                '价格相关': '💰',
                '时间相关': '⏰',
                '效果相关': '🎯',
                '回家商量': '🏠',
                '竞品对比': '🆚',
                '用户体验': '😊',
                '决策流程': '📋',
                '信任相关': '🔒',
                '产品效果': '✨'
            };
            return emojiMap[category] || '📌';
        }

        // 过滤并渲染
        function filterAndRender() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();

            filteredObjections = allObjections.filter(obj => {
                const matchCategory = selectedCategory === 'all' || obj.category === selectedCategory;
                const matchSearch = !searchTerm ||
                    obj.description?.toLowerCase().includes(searchTerm) ||
                    obj.title?.toLowerCase().includes(searchTerm) ||
                    obj.keywords?.some(k => k.toLowerCase().includes(searchTerm));

                return matchCategory && matchSearch;
            });

            renderObjections();
        }

        // 渲染异议
        function renderObjections() {
            const container = document.getElementById('objectionList');

            if (filteredObjections.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>没有找到相关异议</h3>
                        <p>尝试修改搜索关键词或选择其他分类</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = filteredObjections.map((obj, idx) => `
                <div class="objection-card" data-id="${obj.id}">
                    <div class="objection-header">
                        <div class="objection-id">${obj.id}</div>
                        <div class="objection-title">${obj.title}</div>
                        <div class="objection-category">${obj.category}</div>
                    </div>

                    <div class="objection-content">
                        <div class="content-section">
                            <div class="content-section-title">❓ 客户异议</div>
                            <div class="content-section-content">${obj.description}</div>
                        </div>

                        ${obj.analysis ? `
                        <div class="content-section">
                            <div class="content-section-title">💡 问题分析</div>
                            <div class="content-section-content">${obj.analysis}</div>
                        </div>
                        ` : ''}

                        <div class="content-section">
                            <div class="content-section-title">🎯 回复方案</div>
                            <ul class="solutions-list">
                                ${(obj.solutions || []).map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>

                        ${obj.dataPoints && obj.dataPoints.length > 0 ? `
                        <div class="content-section">
                            <div class="content-section-title">📊 数据支撑</div>
                            <div class="data-points">
                                ${obj.dataPoints.map(p => `<div>• ${p}</div>`).join('')}
                            </div>
                        </div>
                        ` : ''}

                        ${obj.counterExamples && obj.counterExamples.length > 0 ? `
                        <div class="content-section">
                            <div class="content-section-title">✅ 成功案例</div>
                            <div class="data-points">
                                ${obj.counterExamples.map(e => `<div>• ${e}</div>`).join('')}
                            </div>
                        </div>
                        ` : ''}

                        ${obj.tips && obj.tips.length > 0 ? `
                        <div class="content-section">
                            <div class="content-section-title">💬 销售技巧</div>
                            <div class="tips">
                                ${obj.tips.map(t => `<div>✨ ${t}</div>`).join('')}
                            </div>
                        </div>
                        ` : ''}

                        <button class="copy-btn" onclick="copyToClipboard('${obj.id}')">📋 复制话术</button>
                    </div>
                </div>
            `).join('');

            // 添加点击事件展开/折叠
            document.querySelectorAll('.objection-card').forEach(card => {
                card.addEventListener('click', function(e) {
                    if (e.target.classList.contains('copy-btn')) return;
                    this.classList.toggle('expanded');
                });
            });
        }

        // 复制到剪贴板
        function copyToClipboard(objId) {
            const obj = allObjections.find(o => o.id == objId);
            if (!obj) return;

            const text = `【${obj.title}】\n\n问题：${obj.description}\n\n解决方案：\n${obj.solutions.join('\n')}`;
            
            navigator.clipboard.writeText(text).then(() => {
                const btn = event.target;
                btn.textContent = '✅ 已复制';
                btn.classList.add('copied');
                setTimeout(() => {
                    btn.textContent = '📋 复制话术';
                    btn.classList.remove('copied');
                }, 2000);
            });
        }

        // 事件监听
        function attachEventListeners() {
            document.getElementById('searchInput').addEventListener('input', filterAndRender);

            document.querySelectorAll('.category-item').forEach(item => {
                item.addEventListener('click', function() {
                    document.querySelectorAll('.category-item').forEach(i => i.classList.remove('active'));
                    this.classList.add('active');
                    selectedCategory = this.dataset.category;
                    filterAndRender();
                });
            });
        }

        // 更新时间
        function updateUpdateTime() {
            const now = new Date();
            const time = now.toLocaleString('zh-CN');
            document.getElementById('updateTime').textContent = `更新于 ${time}`;
        }

        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """主页"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/objections')
def api_objections():
    """API 端点 - 获取所有异议"""
    return jsonify(OBJECTIONS)

@app.route('/api/objections/<int:objection_id>')
def api_objection(objection_id):
    """API 端点 - 获取单个异议"""
    for obj in OBJECTIONS:
        if obj['id'] == objection_id:
            return jsonify(obj)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/search', methods=['GET'])
def api_search():
    """API 端点 - 搜索异议"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')

    results = [
        obj for obj in OBJECTIONS
        if (query in obj.get('description', '').lower() or
            query in obj.get('title', '').lower() or
            any(query in k.lower() for k in obj.get('keywords', [])))
        and (not category or obj.get('category') == category)
    ]

    return jsonify(results)

@app.route('/api/stats')
def api_stats():
    """API 端点 - 获取统计信息"""
    categories = list(set(obj['category'] for obj in OBJECTIONS))
    return jsonify({
        'total': len(OBJECTIONS),
        'categories_count': len(categories),
        'categories': categories,
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║     🐿️ 松鼠AI 异议查询助手 - Web 应用已启动               ║
    ╚════════════════════════════════════════════════════════════════╝

    📊 统计信息:
      • 总异议数: {} 条
      • 异议分类: {} 类

    🚀 访问地址:
      • 本地: http://127.0.0.1:5000
      • 局域网: http://<your-ip>:5000

    📡 API 端点:
      • GET  /api/objections         - 获取所有异议
      • GET  /api/objections/<id>    - 获取单个异议
      • GET  /api/search?q=...       - 搜索异议
      • GET  /api/stats              - 获取统计信息

    💡 提示:
      按 Ctrl+C 停止服务

    """.format(
        len(OBJECTIONS),
        len(set(obj['category'] for obj in OBJECTIONS))
    ))

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
