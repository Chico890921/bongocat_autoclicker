#!/usr/bin/env python3
# coding: utf-8
"""
BongoCat AutoClicker - 透過 SendInput API 發送真實點擊事件
使用 KivyMD 界面
"""
import ctypes
from ctypes import wintypes
import time
import statistics
import threading

from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '580')
Config.set('graphics', 'resizable', False)

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase
import os

# Windows API 結構與常數
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    )

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    )

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (
            ("mi", MOUSEINPUT),
            ("ki", KEYBDINPUT)
        )
    _anonymous_ = ("_input",)
    _fields_ = (
        ("type", wintypes.DWORD),
        ("_input", _INPUT)
    )

class InputSimulator:
    def __init__(self):
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self.INPUT_MOUSE = 0
        self.MOUSEEVENTF_LEFTDOWN = 0x0002
        self.MOUSEEVENTF_LEFTUP = 0x0004
    
    def click_mouse(self):
        """模擬滑鼠左鍵點擊（不移動游標）"""
        down = INPUT(type=self.INPUT_MOUSE, mi=MOUSEINPUT(dwFlags=self.MOUSEEVENTF_LEFTDOWN))
        self.user32.SendInput(1, ctypes.byref(down), ctypes.sizeof(down))
        
        time.sleep(0.035)
        
        up = INPUT(type=self.INPUT_MOUSE, mi=MOUSEINPUT(dwFlags=self.MOUSEEVENTF_LEFTUP))
        self.user32.SendInput(1, ctypes.byref(up), ctypes.sizeof(up))

# 註冊自訂字體（必須在 App 初始化之前）
def register_fonts():
    """註冊自訂字體"""
    fonts_path = os.path.join(os.path.dirname(__file__), 'fonts')
    
    # 註冊英文字體 Montserrat
    montserrat_path = os.path.join(fonts_path, 'Montserrat-VariableFont_wght.ttf')
    if os.path.exists(montserrat_path):
        LabelBase.register(name='Montserrat', fn_regular=montserrat_path)
        print('✅ 成功載入 Montserrat 字體')
    
    # 註冊中文字體 Shippori Antique
    shippori_path = os.path.join(fonts_path, 'ShipporiAntiqueB1-Regular.ttf')
    if os.path.exists(shippori_path):
        LabelBase.register(name='ShipporiAntique', fn_regular=shippori_path)
        print('✅ 成功載入 ShipporiAntique 字體')
    
    # 註冊 Segoe UI Emoji 來支援 Emoji 符號
    emoji_font = 'C:/Windows/Fonts/seguiemj.ttf'
    if os.path.exists(emoji_font):
        LabelBase.register(name='Emoji', fn_regular=emoji_font)
        print('✅ 成功載入 Emoji 字體')
    
    # 將 ShipporiAntique 設為預設字體（Roboto 是 KivyMD 的預設字體名稱）
    if os.path.exists(shippori_path):
        LabelBase.register(
            name='Roboto',
            fn_regular=shippori_path,
            fn_bold=shippori_path,
            fn_italic=shippori_path,
            fn_bolditalic=shippori_path
        )
        print('✅ 將 ShipporiAntique 設為預設字體')

class BongoCatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.simulator = InputSimulator()
        self.active = False
        self.click_event = None
        self.interval = 0.1
        self.theme_mode = 'mocha'
        
        # 保存需要更新顏色的元件
        self.screen = None
        self.main_layout = None
        self.title_label = None
        self.subtitle_label = None
        self.status_title = None
        self.settings_title = None
        self.interval_label = None
        self.interval_unit = None
        self.settings_card = None
        self.test_result_label = None
        self.test_button = None
        self.testing = False
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        
        self.screen = MDScreen(md_bg_color=self.get_color('base'))
        
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            padding='20dp',
            spacing='20dp',
            md_bg_color=self.get_color('base')
        )
        
        # 標題（使用 markup 為不同部分指定字體）
        self.title_label = MDLabel(
            text='[font=Emoji]🐱[/font] BongoCat Auto Clicker',
            markup=True,
            font_style='H4',
            halign='center',
            size_hint_y=None,
            height='60dp',
            theme_text_color='Custom',
            text_color=self.get_color('text')
        )
        self.main_layout.add_widget(self.title_label)
        
        self.subtitle_label = MDLabel(
            text='將滑鼠移到下方卡片上啟動自動點擊',
            markup=True,
            font_style='Caption',
            halign='center',
            size_hint_y=None,
            height='30dp',
            theme_text_color='Custom',
            text_color=self.get_color('subtext0')
        )
        self.main_layout.add_widget(self.subtitle_label)
        
        # 狀態卡片
        self.status_card = MDCard(
            orientation='vertical',
            padding='40dp',
            size_hint_y=None,
            height='200dp',
            md_bg_color=self.get_color('surface0'),
            elevation=2
        )
        
        self.status_title = MDLabel(
            text='[font=Emoji]🎯[/font] 自動點擊狀態',
            markup=True,
            font_style='Subtitle1',
            halign='center',
            size_hint_y=None,
            height='30dp',
            theme_text_color='Custom',
            text_color=self.get_color('lavender')
        )
        self.status_card.add_widget(self.status_title)
        
        self.status_label = MDLabel(
            text='[font=Emoji]⚪[/font] 待機中',
            markup=True,
            font_style='H3',
            halign='center',
            theme_text_color='Custom',
            text_color=self.get_color('text')
        )
        self.status_card.add_widget(self.status_label)
        
        Window.bind(mouse_pos=self.on_mouse_pos)
        
        self.main_layout.add_widget(self.status_card)
        
        # 設定卡片
        self.settings_card = MDCard(
            orientation='vertical',
            padding='20dp',
            size_hint_y=None,
            height='200dp',
            md_bg_color=self.get_color('surface0'),
            elevation=2
        )
        
        self.settings_title = MDLabel(
            text='[font=Emoji]⚙️[/font] 設定: 輸入完後按 Enter 鍵',
            markup=True,
            font_style='Subtitle1',
            size_hint_y=None,
            height='30dp',
            theme_text_color='Custom',
            text_color=self.get_color('lavender')
        )
        self.settings_card.add_widget(self.settings_title)
        
        interval_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp',
            padding=['0dp', '10dp', '0dp', '0dp']
        )
        
        self.interval_label = MDLabel(
            text='點擊間隔:',
            markup=True,
            size_hint_x=None,
            width='100dp',
            theme_text_color='Custom',
            text_color=self.get_color('text')
        )
        interval_layout.add_widget(self.interval_label)
        
        self.interval_field = MDTextField(
            text='0.1',
            size_hint_x=None,
            width='100dp',
            hint_text='秒',
            mode='round',
            on_text_validate=self.update_interval
        )
        interval_layout.add_widget(self.interval_field)
        
        self.interval_unit = MDLabel(
            text='秒',
            markup=True,
            size_hint_x=None,
            width='50dp',
            theme_text_color='Custom',
            text_color=self.get_color('text')
        )
        interval_layout.add_widget(self.interval_unit)
        
        # 填充空間
        interval_layout.add_widget(MDLabel(text=''))
        
        # 主題切換按鈕
        self.theme_button = MDIconButton(
            icon='weather-night',
            pos_hint={'center_y': 0.5},
            on_release=self.toggle_theme
        )
        interval_layout.add_widget(self.theme_button)
        
        self.settings_card.add_widget(interval_layout)
        
        # 測試按鈕區域
        test_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='40dp',
            spacing='10dp',
            padding=['0dp', '10dp', '0dp', '0dp']
        )
        
        self.test_button = MDRaisedButton(
            text='測試速度',
            size_hint_x=None,
            width='120dp',
            on_release=self.start_speed_test,
            md_bg_color=self.get_color('mauve')
        )
        test_layout.add_widget(self.test_button)
        
        # 填充空間
        test_layout.add_widget(MDLabel(text=''))
        
        self.settings_card.add_widget(test_layout)
        
        # 測試結果顯示
        self.test_result_label = MDLabel(
            text='',
            markup=True,
            size_hint_y=None,
            height='30dp',
            theme_text_color='Custom',
            text_color=self.get_color('mauve'),
            halign='left'
        )
        self.test_result_label.bind(size=self.test_result_label.setter('text_size'))
        self.settings_card.add_widget(self.test_result_label)
        
        self.main_layout.add_widget(self.settings_card)
        
        self.screen.add_widget(self.main_layout)
        return self.screen
    
    def get_color(self, name):
        """獲取 Catppuccin 配色"""
        if self.theme_mode == 'mocha':
            colors = {
                'base': (0.118, 0.118, 0.184, 1),
                'surface0': (0.192, 0.196, 0.263, 1),
                'text': (0.804, 0.839, 0.957, 1),
                'subtext0': (0.651, 0.678, 0.784, 1),
                'lavender': (0.706, 0.749, 0.996, 1),
                'mauve': (0.678, 0.518, 0.867, 1),  # 更深的紫色
            }
        else:
            colors = {
                'base': (0.937, 0.945, 0.961, 1),
                'surface0': (0.8, 0.816, 0.855, 1),
                'text': (0.298, 0.310, 0.412, 1),
                'subtext0': (0.424, 0.435, 0.522, 1),
                'lavender': (0.447, 0.529, 0.992, 1),
                'mauve': (0.451, 0.184, 0.800, 1),  # 更深的紫色
            }
        return colors.get(name, (1, 1, 1, 1))
    
    def on_mouse_pos(self, window, pos):
        """檢測滑鼠是否在狀態卡片上"""
        if self.status_card.collide_point(*pos):
            if not self.active:
                self.start_clicking()
        else:
            if self.active:
                self.stop_clicking()
    
    def start_clicking(self):
        """開始自動點擊"""
        self.active = True
        self.status_label.text = '[font=Emoji]🟢[/font] 執行中'
        self.click_event = Clock.schedule_interval(self.do_click, self.interval)
    
    def stop_clicking(self):
        """停止自動點擊"""
        self.active = False
        self.status_label.text = '[font=Emoji]⚪[/font] 待機中'
        if self.click_event:
            self.click_event.cancel()
    
    def do_click(self, dt):
        """執行點擊"""
        try:
            self.simulator.click_mouse()
        except Exception as e:
            print(f'Error: {e}')
    
    def update_interval(self, instance):
        """更新點擊間隔"""
        try:
            self.interval = max(0.001, float(self.interval_field.text))
            if self.active:
                self.stop_clicking()
                self.start_clicking()
        except ValueError:
            self.interval_field.text = str(self.interval)
    
    def toggle_theme(self, instance):
        """切換主題"""
        if self.theme_mode == 'mocha':
            self.theme_mode = 'latte'
            self.theme_cls.theme_style = "Light"
            self.theme_button.icon = 'weather-sunny'
        else:
            self.theme_mode = 'mocha'
            self.theme_cls.theme_style = "Dark"
            self.theme_button.icon = 'weather-night'
        
        # 更新所有顏色
        self.update_theme_colors()
    
    def update_theme_colors(self):
        """更新所有元件的顏色"""
        # 更新背景顏色
        self.screen.md_bg_color = self.get_color('base')
        self.main_layout.md_bg_color = self.get_color('base')
        
        # 更新卡片背景
        self.status_card.md_bg_color = self.get_color('surface0')
        self.settings_card.md_bg_color = self.get_color('surface0')
        
        # 更新文字顏色
        self.title_label.text_color = self.get_color('text')
        self.subtitle_label.text_color = self.get_color('subtext0')
        self.status_title.text_color = self.get_color('lavender')
        self.status_label.text_color = self.get_color('text')
        self.settings_title.text_color = self.get_color('lavender')
        self.interval_label.text_color = self.get_color('text')
        self.interval_unit.text_color = self.get_color('text')
        if self.test_result_label:
            self.test_result_label.text_color = self.get_color('mauve')
        if self.test_button:
            self.test_button.md_bg_color = self.get_color('mauve')
    
    def start_speed_test(self, instance):
        """開始速度測試"""
        if self.testing:
            return
        
        self.testing = True
        self.test_button.disabled = True
        self.test_button.text = '測試中...'
        self.test_result_label.text = '[font=Emoji]⏳[/font] 正在測試，請稍候...'
        
        # 在背景執行緒中執行測試
        thread = threading.Thread(target=self.run_speed_test, daemon=True)
        thread.start()
    
    def run_speed_test(self):
        """執行速度測試（在背景執行緒中）"""
        try:
            # 測試不同間隔
            test_intervals = [0.01, 0.02, 0.05, 0.1]
            best_interval = None
            best_efficiency = 0
            
            for interval in test_intervals:
                num_clicks = 30
                actual_intervals = []
                
                start_time = time.perf_counter()
                last_click_time = start_time
                
                for i in range(num_clicks):
                    click_start = time.perf_counter()
                    self.simulator.click_mouse()
                    
                    if i > 0:
                        actual_intervals.append(click_start - last_click_time)
                    
                    last_click_time = click_start
                    
                    if i < num_clicks - 1:
                        elapsed = time.perf_counter() - click_start
                        sleep_time = max(0, interval - elapsed)
                        if sleep_time > 0:
                            time.sleep(sleep_time)
                
                end_time = time.perf_counter()
                total_time = end_time - start_time
                
                # 計算效率
                actual_cps = num_clicks / total_time
                theoretical_cps = 1 / interval
                efficiency = (actual_cps / theoretical_cps) * 100
                
                # 找到效率 >= 95% 的最小間隔
                if efficiency >= 95 and (best_interval is None or interval < best_interval):
                    best_interval = interval
                    best_efficiency = efficiency
            
            # 更新 UI（在主執行緒中）
            if best_interval:
                Clock.schedule_once(
                    lambda dt: self.show_test_result(best_interval, best_efficiency), 0
                )
            else:
                Clock.schedule_once(
                    lambda dt: self.show_test_result(0.1, 0), 0
                )
        
        except Exception as e:
            print(f'測試錯誤: {e}')
            Clock.schedule_once(
                lambda dt: self.show_test_error(), 0
            )
    
    def show_test_result(self, interval, efficiency):
        """顯示測試結果"""
        interval_ms = interval * 1000
        cps = 1 / interval
        
        if efficiency > 0:
            self.test_result_label.text = f'[font=Emoji]✅[/font] 建議最低間隔: {interval} 秒 ({interval_ms:.0f}ms, {cps:.0f} 點擊/秒)'
        else:
            self.test_result_label.text = '[font=Emoji]⚠️[/font]  建議使用預設值 0.1 秒'
        
        self.test_button.disabled = False
        self.test_button.text = '測試速度'
        self.testing = False
    
    def show_test_error(self):
        """顯示測試錯誤"""
        self.test_result_label.text = '[font=Emoji]❌[/font] 測試失敗，請重試'
        self.test_button.disabled = False
        self.test_button.text = '測試速度'
        self.testing = False

if __name__ == '__main__':
    register_fonts()  # 先註冊字體
    BongoCatApp().run()
