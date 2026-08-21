import json
from datetime import datetime, timedelta
import requests

API_URL = "https://ecampus.ncfu.ru/schedule/GetSchedule"
GROUP_ID = 19931  # ИНС-б-о-26-2

def get_monday(date: datetime) -> datetime:
    return date - timedelta(days=date.weekday())

def fetch_schedule_for_date(target_date: datetime):
    monday = get_monday(target_date)
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
        print(f"Ошибка на дату {date_str}: {e}")
        return []

def main():
    today = datetime.now()
    
    # Стартуем с начала учебного года (первый понедельник сентября)
    start_year = today.year
    start_september = datetime(start_year, 9, 1)
    base_monday = get_monday(start_september)
    if base_monday.month < 9:
        base_monday += timedelta(days=7)

    # Скачиваем на 18 недель семестра вперед
    weeks_data = {}
    for week_num in range(1, 19):
        current_monday = base_monday + timedelta(weeks=week_num - 1)
        monday_key = current_monday.strftime("%Y-%m-%d")
        print(f"Загрузка недели {week_num} ({monday_key})...")
        week_schedule = fetch_schedule_for_date(current_monday)
        weeks_data[monday_key] = {
            "week_number": week_num,
            "monday": monday_key,
            "days": week_schedule
        }

    full_data = {
        "updated_at": today.strftime("%Y-%m-%d %H:%M:%S"),
        "group_id": GROUP_ID,
        "weeks": weeks_data
    }
    
    with open("schedule.json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)
        
    print("Семестр успешно выгружен в schedule.json")

if __name__ == "__main__":
    main()
