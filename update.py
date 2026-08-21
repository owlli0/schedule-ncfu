import json
from datetime import datetime, timedelta
import requests

API_URL = "https://ecampus.ncfu.ru/schedule/GetSchedule"
GROUP_ID = 19931  # ID группы ИНС-б-о-26-2

def get_monday(date: datetime) -> datetime:
    """Возвращает понедельник недели для переданной даты"""
    return date - timedelta(days=date.weekday())

def fetch_schedule_for_date(target_date: datetime):
    monday = get_monday(target_date)
    # Формат даты, который ожидает сервер СКФУ
    date_str = monday.strftime("%Y-%m-%dT00:00:00.000Z")
    
    payload = {
        "date": date_str,
        "Id": GROUP_ID,
        "targetType": 2
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при получении расписания на {date_str}: {e}")
        return []

def main():
    today = datetime.now()
    
    # Скачиваем текущую и следующую неделю
    current_week_data = fetch_schedule_for_date(today)
    next_week_data = fetch_schedule_for_date(today + timedelta(days=7))
    
    full_data = {
        "updated_at": today.strftime("%Y-%m-%d %H:%M:%S"),
        "group_id": GROUP_ID,
        "current_week": current_week_data,
        "next_week": next_week_data
    }
    
    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
        
    print("Расписание успешно сохранено в schedule.json")

if __name__ == "__main__":
    main()
