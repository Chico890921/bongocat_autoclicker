# 🐱 BongoCat Auto Clicker

**一個基於 Python 和 KivyMD 的自動點擊工具，使用 Windows SendInput API 發送真實的滑鼠點擊事件。**

## 📹 Demo
![](/assets/demo.mp4)

> 💡 如果影片無法播放，請直接查看 [assets/demo.mp4](assets/demo.mp4)


## ✨ 特色功能

- 🎯 **滑鼠懸停啟動** - 將滑鼠移到狀態卡片上即可自動開始點擊
- ⚙️ **自訂點擊間隔** - 支援從 0.001 秒到任意間隔的自由設定
- 🚀 **速度測試** - 自動測試系統最佳點擊間隔，找出效率 ≥ 95% 的最快速度
- 🌓 **雙主題切換** - Catppuccin Mocha (深色) 和 Latte (淺色) 主題
- 🎨 **自訂字體** - 使用 Montserrat (英文) 和 Shippori Antique B1 (中文) 字體
- 💻 **真實點擊事件** - 使用 Windows SendInput API，模擬真實滑鼠操作

## 📋 系統需求

- **作業系統**: Windows 10/11
- **Python**: 3.11
- **依賴套件**:
  - KivyMD 1.2.0
  - Kivy 2.3.1
  - PyWin32

## 🚀 快速開始

### 方法一：執行 EXE 檔案 (推薦)

1. 前往 [Releases](https://github.com/Chico890921/bongocat_autoclicker/releases) 頁面下載最新版本的 `BongoCat_AutoClicker.exe`
2. 雙擊執行即可使用

### 方法二：從原始碼執行

1. **克隆專案**
   ```bash
   git clone https://github.com/Chico890921/bongocat_autoclicker.git
   cd bongocat_autoclicker
   ```

2. **建立虛擬環境**
   ```bash
   python -m venv venv_py311
   venv_py311\Scripts\activate
   ```

3. **安裝依賴**
   ```bash
   pip install kivymd>=1.2.0 kivy>=2.3.1 pywin32
   ```

4. **執行程式**
   ```bash
   python BongoCat_AutoClicker.py
   ```

## 📖 使用說明

### 基本操作

1. **啟動自動點擊**
   - 將滑鼠游標移到「🎯 自動點擊狀態」卡片上
   - 狀態會從「⚪ 待機中」變為「🟢 執行中」
   - 程式會以設定的間隔自動點擊

2. **停止自動點擊**
   - 將滑鼠移出狀態卡片區域即可停止

3. **調整點擊間隔**
   - 在「點擊間隔」欄位輸入數值 (單位：秒)
   - 按下 Enter 鍵確認
   - 最小值為 0.001 秒

4. **速度測試**
   - 點擊「測試速度」按鈕
   - 程式會自動測試 0.01s、0.02s、0.05s、0.1s 四個間隔
   - 測試完成後會顯示建議的最低間隔 (效率 ≥ 95%)

5. **切換主題**
   - 點擊右上角的太陽/月亮圖示
   - 在深色 (Mocha) 和淺色 (Latte) 主題間切換


## 🛠️ 打包成 EXE

專案提供自動打包腳本：

```bash
# 執行打包腳本
.\build.bat
```

或手動打包：

```bash
# 啟動虛擬環境
venv_py311\Scripts\activate

# 安裝 PyInstaller
pip install pyinstaller

# 執行打包
pyinstaller BongoCat_AutoClicker.spec --noconfirm
```

生成的 EXE 檔案位於 `dist/BongoCat_AutoClicker.exe`

## 📁 專案結構

```
bongocat_autoclicker/
├── BongoCat_AutoClicker.py         # 主程式 (KivyMD 版本)
├── BongoCat_AutoClicker.spec       # PyInstaller 配置
├── build.bat                       # 打包批次檔
├── LICENSE.txt                     # 授權文件
├── README.md                       # 說明文件
├── assets/                         # 資源資料夾
│   ├── demo.mp4                    # 示範影片
├── fonts/                          # 字體資料夾
│   ├── Montserrat-VariableFont_wght.ttf
│   └── ShipporiAntiqueB1-Regular.ttf
└── dist/                           # 打包輸出資料夾 (執行 build.bat 後生成)
    └── BongoCat_AutoClicker.exe
```

## 🎨 配色方案

使用 [Catppuccin](https://github.com/catppuccin/catppuccin) 配色：

### Mocha (深色主題)
- Base: `#1e1e2e`
- Surface: `#313244`
- Text: `#cdd6f4`
- Mauve: `#cba6f7`
- Lavender: `#b4befe`

### Latte (淺色主題)
- Base: `#eff1f5`
- Surface: `#ccd0da`
- Text: `#4c4f69`
- Mauve: `#8839ef`
- Lavender: `#7287fd`

## ⚠️ 注意事項

1. **僅限 Windows** - 程式使用 Windows SendInput API，不支援其他作業系統
2. **管理員權限** - 某些應用程式可能需要管理員權限才能接收點擊事件
3. **遊戲反作弊** - 部分遊戲的反作弊系統可能會偵測到自動點擊，請謹慎使用



## 📝 授權

> You can check out the full license [here](LICENSE)

This project is licensed under the terms of the **GNU General Public License v3.0** (or any later version).


## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📧 聯絡

如有問題或建議，歡迎開啟 Issue 討論。
