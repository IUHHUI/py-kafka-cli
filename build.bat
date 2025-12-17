@echo off
REM Kafka CLI 构建脚本 (Windows)

echo =========================================
echo   Kafka CLI 构建脚本
echo =========================================
echo.

REM 检查 Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.7+
    exit /b 1
)

python --version
echo.

REM 安装依赖
echo 📦 安装依赖...
python -m pip install -r requirements.txt -q
echo ✓ 依赖安装完成
echo.

REM 清理旧的构建文件
echo 🧹 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✓ 清理完成
echo.

REM 使用 PyInstaller 构建
echo 🔨 开始构建可执行文件...
python -m PyInstaller kafka-cli.spec --clean
echo.

REM 检查构建结果
if exist "dist\kafka-cli.exe" (
    echo =========================================
    echo   ✅ 构建成功！
    echo =========================================
    echo.
    echo 可执行文件位置: dist\kafka-cli.exe
    echo.
    echo 测试运行:
    dist\kafka-cli.exe --help
    echo.
    echo =========================================
    echo   使用方法:
    echo =========================================
    echo.
    echo 1. 直接运行:
    echo    dist\kafka-cli.exe list -b localhost:9092
    echo.
    echo 2. 添加到 PATH 环境变量后:
    echo    kafka-cli --help
    echo.
) else (
    echo ❌ 构建失败，请检查错误信息
    exit /b 1
)
