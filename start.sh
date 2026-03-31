#!/bin/bash

# 松鼠AI 异议查询助手 - 快速启动脚本

echo "=========================================="
echo "🎯 松鼠AI 销售异议查询助手"
echo "=========================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3，请先安装"
    exit 1
fi

echo "✅ Python 版本："
python3 --version
echo ""

# 询问启动方式
echo "请选择启动方式："
echo "1️⃣  Web 版本（推荐给销售）- 直接打开 HTML"
echo "2️⃣  API 服务 - 部署为服务"
echo "3️⃣  Python 脚本 - 数据管理"
echo ""
read -p "请输入选项 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🌐 启动 Web 服务..."
        echo "访问地址: http://localhost:8000/objection_assistant.html"
        echo ""
        echo "按 Ctrl+C 停止服务"
        echo ""
        python3 -m http.server 8000
        ;;
    2)
        echo ""
        echo "📦 检查依赖..."
        
        # 检查是否已安装依赖
        python3 -c "import flask" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "📥 安装依赖..."
            pip install -r requirements.txt
        else
            echo "✅ 依赖已安装"
        fi
        
        echo ""
        echo "🚀 启动 API 服务..."
        echo "访问地址: http://localhost:5000"
        echo "API 文档: http://localhost:5000/"
        echo ""
        echo "按 Ctrl+C 停止服务"
        echo ""
        python3 api_server.py
        ;;
    3)
        echo ""
        echo "📦 检查依赖..."
        
        # 检查是否已安装依赖
        python3 -c "import openpyxl" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "📥 安装依赖..."
            pip install -r requirements.txt
        else
            echo "✅ 依赖已安装"
        fi
        
        echo ""
        echo "🐍 运行 Python 脚本..."
        echo ""
        python3 objection_assistant.py
        ;;
    *)
        echo "❌ 无效的选项"
        exit 1
        ;;
esac
