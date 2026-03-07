#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例58：天气穿搭推荐
根据天气和日历推荐穿搭
"""

import subprocess
import json
from datetime import datetime

CITY = "Shanghai"

def get_weather():
    """获取天气"""
    try:
        result = subprocess.run(
            ["curl", "-s", f"wttr.in/{CITY}?format=j1"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        data = json.loads(result.stdout)
        current = data["current_condition"][0]
        
        return {
            "temp": int(current["temp_C"]),
            "weather": current["weatherDesc"][0]["value"],
            "wind": int(current["windspeedKmph"])
        }
    except Exception as e:
        print(f"获取天气失败: {e}")
        return None

def recommend_outfit(weather_data):
    """推荐穿搭"""
    temp = weather_data["temp"]
    weather = weather_data["weather"]
    wind = weather_data["wind"]
    
    recommendations = []
    
    # 温度判断
    if temp < 5:
        recommendations.append("🧥 羽绒服 + 保暖内衣")
    elif temp < 15:
        recommendations.append("🥼 轻薄外套 + 长袖")
    elif temp < 25:
        recommendations.append("👕 长袖T恤 + 牛仔裤")
    else:
        recommendations.append("👕 短袖 + 轻薄裤")
    
    # 天气判断
    if "Rain" in weather or "雨" in weather:
        recommendations.append("🌂 带伞")
    if "Snow" in weather or "雪" in weather:
        recommendations.append("🥾 防滑鞋")
    if wind > 30:
        recommendations.append("🧣 防风")
    
    return recommendations

def main():
    print("="*50)
    print("👗 今日穿搭推荐")
    print("="*50)
    
    weather = get_weather()
    
    if not weather:
        print("❌ 无法获取天气")
        return
    
    print(f"\n🌤️ 天气: {weather['weather']}")
    print(f"🌡️ 温度: {weather['temp']}°C")
    print(f"💨 风速: {weather['wind']} km/h")
    
    outfits = recommend_outfit(weather)
    
    print("\n👕 推荐穿搭:")
    for outfit in outfits:
        print(f"   {outfit}")

if __name__ == "__main__":
    main()
