@echo off
chcp 65001 >nul
echo.
echo 🐱 BongoCat AutoClicker - 打包工具
echo ============================================================
echo.

REM 檢查虛擬環境
if not exist ".venv\Scripts\python.exe" (
    echo ❌ 找不到虛擬環境！
    echo 請確認 .venv 資料夾存在
    pause
    exit /b 1
)

REM 啟動虛擬環境並安裝 PyInstaller
echo 📦 安裝 PyInstaller...
.venv\Scripts\python.exe -m pip install pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyInstaller 安裝可能有問題，繼續嘗試打包...
) else (
    echo ✅ PyInstaller 已準備就緒
)

echo.
echo 🔨 開始打包...
echo ============================================================
echo.

REM 使用 spec 文件打包
.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm BongoCat_AutoClicker.spec

if errorlevel 1 (
    echo.
    echo ❌ 打包失敗！
    echo.
    echo 可能的解決方案:
    echo 1. 確認所有依賴套件都已安裝
    echo 2. 嘗試刪除 build 和 dist 資料夾後重試
    echo 3. 檢查是否有防毒軟體阻擋
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ 打包完成！
echo ============================================================
echo.
echo 📁 執行檔位置: dist\BongoCat_AutoClicker.exe
echo 📦 檔案大小: 
dir dist\BongoCat_AutoClicker.exe | find "BongoCat"
echo.
echo 📝 使用說明:
echo 1. 執行 dist\BongoCat_AutoClicker.exe
echo 2. 將滑鼠移到「自動點擊狀態」卡片上開始點擊
echo 3. 移開滑鼠停止點擊
echo.
echo ⚠️  注意: fonts 資料夾已經包含在執行檔中
echo.
pause
