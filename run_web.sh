#!/bin/bash
# 松鼠AI 异议查询助手 - Web 应用启动脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║        🐿️ 松鼠AI 异议查询助手 - Web 应用启动             ║
╚════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 获取当前目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo -e "${YELLOW}[1/5]${NC} 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION${NC}"

echo -e "${YELLOW}[2/5]${NC} 检查依赖包..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}📦 安装 Flask...${NC}"
    pip3 install flask flask-cors -q
fi
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${RED}❌ Flask 安装失败${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 依赖包检查完成${NC}"

echo -e "${YELLOW}[3/5]${NC} 检查数据文件..."
if [ ! -f "objections_db.json" ]; then
    echo -e "${RED}❌ 异议数据库不存在${NC}"
    exit 1
fi
COUNT=$(python3 -c "import json; f=open('objections_db.json'); print(len(json.load(f)))" 2>/dev/null)
echo -e "${GREEN}✓ 已加载 $COUNT 条异议${NC}"

echo -e "${YELLOW}[4/5]${NC} 检查 Web 应用文件..."
if [ ! -f "web_app.py" ]; then
    echo -e "${RED}❌ web_app.py 不存在${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Web 应用文件完整${NC}"

echo -e "${YELLOW}[5/5]${NC} 启动 Web 服务..."
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                   🚀 服务启动成功！                         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📱 访问地址:${NC}"
echo -e "   • 本地访问:   ${GREEN}http://127.0.0.1:5000${NC}"
echo -e "   • 局域网访问: ${GREEN}http://\$(hostname -I | awk '{print \$1}'):5000${NC}"
echo ""
echo -e "${BLUE}📊 数据统计:${NC}"
echo -e "   • 总异议数: $COUNT 条"
echo ""
echo -e "${BLUE}💡 提示:${NC}"
echo -e "   • 按 Ctrl+C 停止服务"
echo -e "   • 访问 http://127.0.0.1:5000/api/stats 查看 API 统计"
echo ""

# 启动服务
python3 web_app.py
