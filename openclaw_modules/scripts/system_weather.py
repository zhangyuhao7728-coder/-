#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统天气数据读取器
直接读取 macOS Weather 应用数据库
"""

import sqlite3
import json

WEATHER_DB = "/Users/zhangyuhao/Library/Weather/weather-data.db"
LOCATION_DB = "/Users/zhangyuhao/Library/Weather/current-location.db"

def get_location():
    """获取当前设置的天气位置"""
    conn = sqlite3.connect(LOCATION_DB)
    cursor = conn.cursor()
    cursor.execute('SELECT id, location, date FROM currentLocationGeocoded')
    row = cursor.fetchone()
    conn.close()
    
    if row and row[1]:
        data = json.loads(row[1])
        return {
            "name": data.get("name", ""),
            "preciseName": data.get("preciseName", ""),
            "lat": data.get("coordinate", {}).get("latitude", 0),
            "lon": data.get("coordinate", {}).get("longitude", 0),
        }
    return None

def get_current_weather():
    """获取当前天气数据"""
    conn = sqlite3.connect(WEATHER_DB)
    cursor = conn.cursor()
    
    # 尝试获取小时预报
    cursor.execute('SELECT key, data, timestamp FROM hourlyForecast LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    
    if row and row[1]:
        try:
            data = json.loads(row[1])
            return data
        except:
            pass
    
    return None

def get_weather_simple():
    """简化天气获取"""
    # 获取位置
    loc = get_location()
    
    # 读取原始数据
    conn = sqlite3.connect(WEATHER_DB)
    cursor = conn.cursor()
    
    # 尝试不同表
    tables = ['hourlyForecast', 'currentWeather', 'dailyForecast']
    
    weather_data = None
    for table in tables:
        try:
            cursor.execute(f'SELECT key, data FROM {table} LIMIT 1')
            row = cursor.fetchone()
            if row and row[1]:
                weather_data = row[1]
                break
        except:
            pass
    
    conn.close()
    
    return {
        "location": loc,
        "raw_data": weather_data[:200] if weather_data else None
    }

if __name__ == "__main__":
    result = get_weather_simple()
    print("=== 系统天气数据 ===")
    print(f"位置: {result['location']['name'] if result['location'] else '未知'}")
    print(f"坐标: {result['location']['lat']}, {result['location']['lon']}")
    print(f"数据: {result['raw_data'][:100] if result['raw_data'] else '无'}")
