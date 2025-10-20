@echo off
chcp 65001 >nul
echo ========================================
echo 数据上报照片上传功能部署脚本
echo ========================================
echo.

echo [1/3] 激活conda环境...
call conda activate deepvisit
if errorlevel 1 (
    echo 错误: 无法激活deepvisit环境
    echo 请确保已创建deepvisit虚拟环境
    pause
    exit /b 1
)
echo ✓ 环境激活成功
echo.

echo [2/3] 运行数据库迁移...
python migrate_add_photo_fields.py
if errorlevel 1 (
    echo 错误: 数据库迁移失败
    pause
    exit /b 1
)
echo ✓ 数据库迁移完成
echo.

echo [3/3] 启动Flask应用...
echo 应用将在 http://localhost:5000 启动
echo 按 Ctrl+C 可停止服务器
echo.
python run.py

pause

