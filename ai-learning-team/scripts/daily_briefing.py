#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 52：每日简报生成器 v4
整合：系统天气位置 + 天气 + 日历
"""

import requests
import sqlite3
import json
import subprocess
from datetime import datetime

WEATHER_DB = "/Users/zhangyuhao/Library/Weather/weather-data.db"
LOCATION_DB = "/Users/zhangyuhao/Library/Weather/current-location.db"

def get_system_location():
    """从系统获取天气位置"""
    conn = sqlite3.connect(LOCATION_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT id, location, date FROM currentLocationGeocoded')
    row = cursor.fetchone()
    conn.close()
    
    if row and row[1]:
        data = json.loads(row[1])
        return {
            "name": data.get("preciseName", data.get("name", "")),
            "lat": data.get("coordinate", {}).get("latitude", 31.23),
            "lon": data.get("coordinate", {}).get("longitude", 121.47),
        }
    return {"name": "上海", "lat": 31.23, "lon": 121.47}

def get_weather(lat, lon):
    """用 Open-Meteo 获取天气"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": lat, "longitude": lon, "current_weather": True, "timezone": "Asia/Shanghai"}
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        w = data.get("current_weather", {})
        
        code_map = {0:"晴",1:"晴间多云",2:"多云",3:"阴",45:"雾",48:"雾凇",51:"小雪",53:"中雪",55:"大雪",61:"小雨",63:"中雨",65:"大雨",71:"小雪",73:"中雪",75:"大雪",80:"阵雨",81:"阵雨",82:"强阵雨",95:"雷暴",96:"雷暴+冰雹",99:"雷暴+大冰雹"}
        
        return {"temp": w.get("temperature","N/A"), "code": w.get("weathercode",0), "desc": code_map.get(w.get("weathercode",0),"未知"), "wind": w.get("windspeed",0)}
    except: return {"temp":"N/A","desc":"获取失败","wind":0}

def get_calendar_events():
    """获取今日日历事件"""
    calendars = ["个人", "工作", "生日"]
    events = []
    
    for cal_name in calendars:
        script = f'''
        tell application "Calendar"
            try
                set myCal to calendar "{cal_name}"
                set todayStart to current date
                set time of todayStart to 0
                set todayEnd to todayStart + 1 * days
                set evts to events of myCal where start date >= todayStart and start date < todayEnd
                set evtNames to {{}}
                repeat with e in evts
                    set end of evtNames to summary of e
                end repeat
                return evtNames
            on error
                return {{}}
            end try
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            for e in result.stdout.strip().split(', '):
                events.append(f"📅 {cal_name}: {e}")
    
    return events

def generate_briefing():
    """生成简报"""
    loc = get_system_location()
    weather = get_weather(loc["lat"], loc["lon"])
    events = get_calendar_events()
    
    event_text = "\n".join(events) if events else "- 今天没有安排事件"
    
    briefing = f"""📋 今日简报 - {datetime.now().strftime('%Y-%m-%d')}

📍 位置: {loc['name']} (系统自动)

🌤️ 天气
- 状况：{weather['desc']}
- 温度：{weather['temp']}°C
- 风速：{weather['wind']} km/h
{"- ☔ 记得带伞！" if weather['code'] >= 51 else ""}

📅 日历
{event_text}

---
由 OpenClaw 用例 52 自动生成"""
    return briefing

if __name__ == "__main__":
    print(generate_briefing())
