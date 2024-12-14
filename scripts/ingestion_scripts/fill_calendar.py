import argparse
import psycopg2
from datetime import datetime, timedelta

# Default start and end dates
DEFAULT_START_DATE = datetime(2013, 1, 1)
DEFAULT_END_DATE = datetime.now()

# Database connection parameters
db_config = {
    'dbname': 'raw_data',              
    'user': 'airflow',                
    'password': 'airflow',            
    'host': 'localhost',  # Use localhost if running from local, or postgres if running from a container
    'port': '5432'                    
}

def generate_calendar_dates(start_date, end_date):
    """
    Generate a list of dictionaries where each dictionary represents a day and its attributes.
    """
    current_date = start_date
    calendar_entries = []
    
    while current_date <= end_date:
        year = current_date.year
        quarter = (current_date.month - 1) // 3 + 1
        month = current_date.month
        week = current_date.isocalendar()[1]
        day = current_date.day
        date_time = datetime(year, month, day)  # Start of the day timestamp
        year_week = f"{year}-W{week:02d}"
        
        calendar_entries.append({
            'calendar_year': year,
            'calendar_quarter': quarter,
            'calendar_month': month,
            'calendar_week': week,
            'calendar_day': day,
            'date_time': date_time,
            'calendar_year_week': year_week
        })
        
        current_date += timedelta(days=1)
    
    return calendar_entries

def insert_calendar_entries(conn, calendar_entries):
    """
    Insert the generated calendar entries into the calendar table.
    """
    with conn.cursor() as cursor:
        insert_query = """
        INSERT INTO calendar (calendar_year, calendar_quarter, calendar_month, calendar_week, calendar_day, date_time, calendar_year_week)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for entry in calendar_entries:
            cursor.execute(insert_query, (
                entry['calendar_year'], 
                entry['calendar_quarter'], 
                entry['calendar_month'], 
                entry['calendar_week'], 
                entry['calendar_day'], 
                entry['date_time'], 
                entry['calendar_year_week']
            ))
    conn.commit()

def main(start_date, end_date):
    """
    Main function to generate and insert calendar entries into the database.
    """
    try:
        conn = psycopg2.connect(**db_config)
        
        print(f"Generating calendar entries from {start_date} to {end_date}...")
        calendar_entries = generate_calendar_dates(start_date, end_date)
        
        print(f"Inserting {len(calendar_entries)} entries into the database...")
        insert_calendar_entries(conn, calendar_entries)
        
        print("Calendar successfully filled.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill calendar table with dates from start_date to end_date.")
    parser.add_argument(
        '--start_date', 
        type=lambda s: datetime.strptime(s, '%Y-%m-%d'), 
        default=DEFAULT_START_DATE, 
        help="Start date in YYYY-MM-DD format (default: 2013-01-01)"
    )
    parser.add_argument(
        '--end_date', 
        type=lambda s: datetime.strptime(s, '%Y-%m-%d'), 
        default=DEFAULT_END_DATE, 
        help="End date in YYYY-MM-DD format (default: today's date)"
    )
    
    args = parser.parse_args()
    main(args.start_date, args.end_date)
