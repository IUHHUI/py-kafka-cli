#!/bin/bash
# Kafka CLI 构建脚本 (Linux/macOS)

set -e

echo "========================================="
echo "  Kafka CLI 构建脚本"
echo "========================================="
echo ""

# 检查 Python
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ 错误: 未找到 Python，请先安装 Python 3.7+"
        exit 1
    fi
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "✓ 使用 Python: $($PYTHON_CMD --version)"
echo ""

# 检查并安装依赖
echo "📦 安装依赖..."
$PYTHON_CMD -m pip install -r requirements.txt -q
echo "✓ 依赖安装完成"
echo ""

# 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
rm -rf build dist
echo "✓ 清理完成"
echo ""

# 使用 PyInstaller 构建
echo "🔨 开始构建可执行文件..."
$PYTHON_CMD -m PyInstaller kafka-cli.spec --clean
echo ""

# 检查构建结果
if [ -f "dist/kafka-cli" ]; then
    echo "========================================="
    echo "  ✅ 构建成功！"
    echo "========================================="
    echo ""
    echo "可执行文件位置: dist/kafka-cli"
    echo ""
    echo "测试运行:"
    ./dist/kafka-cli --help
    echo ""
    echo "文件大小:"
    ls -lh dist/kafka-cli | awk '{print $5, $9}'
    echo ""
    echo "========================================="
    echo "  使用方法:"
    echo "========================================="
    echo ""
    echo "1. 直接运行:"
    echo "   ./dist/kafka-cli list -b localhost:9092"
    echo ""
    echo "2. 复制到系统路径:"
    echo "   sudo cp dist/kafka-cli /usr/local/bin/"
    echo "   kafka-cli --help"
    echo ""
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi
