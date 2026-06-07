import time
import requests
import yfinance as yf
from datetime import datetime
from pixoo import Pixoo

# ==================== CONFIGURATION ====================
PIXOO_IP = "192.168.1.153"  # Replace with your Pixoo 64's local IP address
STATION_ID = "A28"          # "A28" is 34 St-Penn Station (A/C/E). Change to your target station ID.
REFRESH_INTERVAL = 30       # Time in seconds between screen refreshes
# =======================================================

# --- AUTOMATED PREMIUM UNIFIED PIXEL FONT ---
CUSTOM_FONT = {
    'A': [(1,0), (2,0), (0,1), (3,1), (0,2), (1,2), (2,2), (3,2), (0,3), (3,3), (0,4), (3,4)],
    'B': [(0,0), (1,0), (2,0), (0,1), (3,1), (0,2), (1,2), (2,2), (0,3), (3,3), (0,4), (1,4), (2,4)],
    'C': [(1,0), (2,0), (3,0), (0,1), (0,2), (0,3), (1,4), (2,4), (3,4)],
    'D': [(0,0), (1,0), (2,0), (0,1), (3,1), (0,2), (3,2), (0,3), (3,3), (0,4), (1,4), (2,4)],
    'E': [(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (0,3), (0,4), (1,4), (2,4), (3,4)],
    'F': [(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (0,3), (0,4)],
    'G': [(1,0), (2,0), (3,0), (0,1), (0,2), (2,2), (3,2), (0,3), (3,3), (1,4), (2,4), (3,4)],
    'H': [(0,0), (3,0), (0,1), (3,1), (0,2), (1,2), (2,2), (3,2), (0,3), (3,3), (0,4), (3,4)],
    'I': [(0,0), (1,0), (2,0), (1,1), (1,2), (1,3), (0,4), (1,4), (2,4)],
    'J': [(3,0), (3,1), (3,2), (0,3), (3,3), (1,4), (2,4)],
    'K': [(0,0), (3,0), (0,1), (2,1), (0,2), (1,2), (0,3), (2,3), (0,4), (3,4)],
    'L': [(1,0), (1,1), (1,2), (1,3), (1,4), (2,4), (3,4)],
    'M': [(0,0), (4,0), (0,1), (1,1), (3,1), (4,1), (0,2), (2,2), (4,2), (0,3), (4,3), (0,4), (4,4)],
    'N': [(0,0), (4,0), (0,1), (1,1), (4,1), (0,2), (2,2), (4,2), (0,3), (3,3), (4,3), (0,4), (4,4)],
    'O': [(1,0), (2,0), (0,1), (3,1), (0,2), (3,2), (0,3), (3,3), (1,4), (2,4)],
    'P': [(0,0), (1,0), (2,0), (0,1), (3,1), (0,2), (1,2), (2,2), (0,3), (0,4)],
    'Q': [(1,0), (2,0), (0,1), (3,1), (0,2), (3,2), (0,3), (2,3), (1,4), (2,4), (3,4), (4,4)],
    'R': [(0,0), (1,0), (2,0), (0,1), (3,1), (0,2), (1,2), (2,2), (0,3), (2,3), (0,4), (3,4)],
    'S': [(1,0), (2,0), (3,0), (0,1), (1,2), (2,2), (3,3), (0,4), (1,4), (2,4)],
    'T': [(0,0), (1,0), (2,0), (1,1), (1,2), (1,3), (1,4)],
    'U': [(0,0), (3,0), (0,1), (3,1), (0,2), (3,2), (0,3), (3,3), (1,4), (2,4)],
    'V': [(0,0), (3,0), (0,1), (3,1), (0,2), (3,2), (1,3), (2,3), (1,4), (2,4)],
    'W': [(0,0), (4,0), (0,1), (4,1), (0,2), (2,2), (4,2), (0,3), (2,3), (4,3), (1,4), (3,4)],
    'X': [(0,0), (3,0), (1,1), (2,1), (1,2), (2,2), (0,3), (3,3), (0,4), (3,4)],
    'Y': [(0,0), (2,0), (0,1), (2,1), (1,2), (1,3), (1,4)],
    'Z': [(0,0), (1,0), (2,0), (3,0), (2,1), (1,2), (0,3), (0,4), (1,4), (2,4), (3,4)],
    '0': [(1,0), (2,0), (0,1), (3,1), (0,2), (3,2), (0,3), (3,3), (1,4), (2,4)],
    '1': [(1,0), (0,1), (1,1), (1,2), (1,3), (0,4), (1,4), (2,4)],
    '2': [(0,0), (1,0), (2,0), (3,0), (3,1), (0,2), (1,2), (2,2), (3,2), (0,3), (0,4), (1,4), (2,4), (3,4)],
    '3': [(0,0), (1,0), (2,0), (3,0), (3,1), (1,2), (2,2), (3,2), (3,3), (0,4), (1,4), (2,4), (3,4)],
    '4': [(0,0), (3,0), (0,1), (3,1), (0,2), (1,2), (2,2), (3,2), (3,3), (3,4)],
    '5': [(0,0), (1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (3,2), (3,3), (0,4), (1,4), (2,4)],
    '6': [(1,0), (2,0), (3,0), (0,1), (0,2), (1,2), (2,2), (3,2), (0,3), (3,3), (1,4), (2,4)],
    '7': [(0,0), (1,0), (2,0), (3,0), (3,1), (2,2), (1,3), (1,4)],
    '8': [(1,0), (2,0), (0,1), (3,1), (1,2), (2,2), (0,3), (3,3), (1,4), (2,4)],
    '9': [(1,0), (2,0), (0,1), (3,1), (1,2), (2,2), (3,2), (3,3), (1,4), (2,4)],
    '.': [(0,4)],
    '%': [(0,0), (2,0), (2,1), (1,2), (0,3), (0,4), (2,4)],
    '/': [(2,0), (2,1), (1,2), (0,3), (0,4)],
    '▲': [(1,0), (0,1), (1,1), (2,1), (1,2), (1,3), (1,4)],
    '▼': [(1,0), (1,1), (1,2), (0,3), (1,3), (2,3), (1,4)],
    ' ': []
}

def get_text_width(text):
    """Calculates custom text string width dynamically to guarantee pixel alignments."""
    w_map = {'M':5, 'N':5, 'W':5, 'Q':5, 'I':3, 'T':3, 'Y':3, '1':3, '.':1, ' ':2, '%':3, '/':3, '▲':3, '▼':3}
    return sum(w_map.get(c, 4) + 1 for c in text) - 1

def draw_text_custom(pixoo, text, start_x, start_y, color):
    """Draws custom text pixel arrays safely without padding shifts."""
    w_map = {'M':5, 'N':5, 'W':5, 'Q':5, 'I':3, 'T':3, 'Y':3, '1':3, '.':1, ' ':2, '%':3, '/':3, '▲':3, '▼':3}
    current_x = start_x
    for char in text:
        if char in CUSTOM_FONT:
            for dx, dy in CUSTOM_FONT[char]:
                pixoo.draw_pixel((current_x + dx, start_y + dy), color)
            current_x += w_map.get(char, 4) + 1

# --- HYPER-LOCAL HUDSON YARDS DATA MODULES ---
def get_weather():
    """Queries Open-Meteo API using exact coordinates for Hudson Yards neighborhood forecasting."""
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=40.7539&longitude=-74.0010&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&hourly=precipitation_probability&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=1"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        
        curr = str(int(round(data['current']['temperature_2m'])))
        high = str(int(round(data['daily']['temperature_2m_max'][0])))
        low = str(int(round(data['daily']['temperature_2m_min'][0])))
        
        current_hour = datetime.now().hour
        rain = str(data['hourly']['precipitation_probability'][current_hour])
        wmo_code = data['current']['weather_code']
        
        if wmo_code in [0]: cond = "clear"
        elif wmo_code in [1, 2]: cond = "partly cloudy"
        elif wmo_code in [3, 45, 48]: cond = "cloudy"
        else: cond = "rain"
            
        return {"curr": curr, "high": high, "low": low, "rain": rain, "cond": cond}
    except Exception as e:
        print(f"Hudson Yards Weather Fetch Error: {e}")
        return {"curr": "--", "high": "--", "low": "--", "rain": "--", "cond": "unknown"}

def get_stocks():
    """Fetches stock trends separating directions into numeric tracking properties."""
    try:
        ticker = yf.Ticker("^GSPC")
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            curr_price = hist['Close'].iloc[-1]
            pct_change = ((curr_price - prev_close) / prev_close) * 100
            
            arrow = "▲" if pct_change >= 0 else "▼"
            return {"perf": f"{abs(pct_change):.2f}%", "arrow": arrow, "up": pct_change >= 0}
    except Exception as e:
        print(f"Stock Fetch Error: {e}")
    return {"perf": "--%", "arrow": "▲", "up": True}

def get_subway_times(stop_id_prefix):
    uptown_times, downtown_times = [], []
    try:
        from nyct_gtfs import NYCTFeed
        feed = NYCTFeed("A")
        now = feed.last_generated if feed.last_generated else datetime.now()
        for trip in feed.trips:
            for update in trip.stop_time_updates:
                if update.stop_id == f"{stop_id_prefix}N":
                    arrival = update.arrival or update.departure
                    if arrival and arrival > now:
                        uptown_times.append(int((arrival - now).total_seconds() / 60))
                elif update.stop_id == f"{stop_id_prefix}S":
                    arrival = update.arrival or update.departure
                    if arrival and arrival > now:
                        downtown_times.append(int((arrival - now).total_seconds() / 60))
        uptown_times = sorted(list(set(uptown_times)))[:3]
        downtown_times = sorted(list(set(downtown_times)))[:3]
    except Exception as e:
        print(f"MTA Subway Fetch Error: {e}")
    return {"uptown": uptown_times, "downtown": downtown_times}

def draw_dotted_line(pixoo, y, color):
    for x in range(0, 64, 2):
        pixoo.draw_pixel((x, y), color)

def draw_large_weather_icon(pixoo, condition, x_min=0, x_max=28, y_min=8, y_max=25):
    """Generates upscaled weather vectors centered strictly inside layout canvas rules."""
    YELLOW, WHITE, GRAY, BLUE = (255, 255, 0), (255, 255, 255), (100, 115, 130), (0, 190, 255)
    pixels = []
    
    if condition == "rain":
        for dx in range(2, 16):
            for dy in range(3, 9): pixels.append((dx, dy, GRAY))
        for dx in range(5, 13):
            for dy in range(1, 3): pixels.append((dx, dy, GRAY))
        pixels.extend([
            (4, 11, BLUE), (4, 13, BLUE),
            (8, 11, BLUE), (8, 13, BLUE),
            (12, 11, BLUE), (12, 13, BLUE)
        ])
    elif condition == "cloudy":
        for dx in range(1, 16):
            for dy in range(4, 11): pixels.append((dx, dy, WHITE))
        for dx in range(4, 13):
            for dy in range(1, 4): pixels.append((dx, dy, WHITE))
    elif condition == "partly cloudy":
        for dx in range(1, 8):
            for dy in range(1, 8): pixels.append((dx, dy, YELLOW))
        for dx in range(5, 17):
            for dy in range(5, 12): pixels.append((dx, dy, WHITE))
        for dx in range(8, 14):
            for dy in range(3, 5): pixels.append((dx, dy, WHITE))
    else:  # clear / sunny
        for dx in range(4, 11):
            for dy in range(4, 11): pixels.append((dx, dy, YELLOW))
        rays = [
            (7, 1), (7, 2), (7, 12), (7, 13),
            (1, 7), (2, 7), (12, 7), (13, 7),
            (3, 3), (11, 3), (3, 11), (11, 11)
        ]
        for dx, dy in rays: pixels.append((dx, dy, YELLOW))
        
    all_dx = [p[0] for p in pixels]
    all_dy = [p[1] for p in pixels]
    
    icon_w = max(all_dx) - min(all_dx) + 1
    icon_h = max(all_dy) - min(all_dy) + 1
    box_w = x_max - x_min + 1
    box_h = y_max - y_min + 1
    
    offset_x = x_min + (box_w - icon_w) // 2 - min(all_dx)
    offset_y = y_min + (box_h - icon_h) // 2 - min(all_dy)
    
    for dx, dy, color in pixels:
        pixoo.draw_pixel((dx + offset_x, dy + offset_y), color)

def draw_mta_bullet(pixoo, letter, start_x, start_y, color):
    WHITE = (255, 255, 255)
    circle = [(2,0),(3,0),(4,0),(1,1),(2,1),(3,1),(4,1),(5,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(1,5),(2,5),(3,5),(4,5),(5,5),(2,6),(3,6),(4,6)]
    for dx, dy in circle: pixoo.draw_pixel((start_x + dx, start_y + dy), color)
    let = []
    if letter == 'A': let = [(3,1), (2,2), (4,2), (2,3), (3,3), (4,3), (2,4), (4,4), (2,5), (4,5)]
    elif letter == 'C': let = [(2,1), (3,1), (4,1), (2,2), (2,3), (2,4), (2,5), (3,5), (4,5)]
    elif letter == 'E': let = [(2,1), (3,1), (4,1), (2,2), (2,3), (3,3), (4,3), (2,4), (2,5), (3,5), (4,5)]
    for dx, dy in let: pixoo.draw_pixel((start_x + dx, start_y + dy), WHITE)

def draw_stationary_train_times(pixoo, times_list, y, color):
    """Draws transit digits centered inside tracking cells right-aligned to column 61."""
    # Shifted left 1 additional pixel so column 3 structurally matches the % sign alignment axis
    slots = [
        {"min_x": 29, "max_x": 37},
        {"min_x": 41, "max_x": 49},
        {"min_x": 53, "max_x": 61}
    ]
    slot_width = 9
    
    # Isolation dots re-centered at columns 39 and 51
    pixoo.draw_pixel((39, y + 4), color)
    pixoo.draw_pixel((51, y + 4), color)
    
    if not times_list:
        dash_w = get_text_width("--")
        draw_text_custom(pixoo, "--", 29 + (33 - dash_w) // 2, y, color)
        return
        
    for i in range(3):
        if i < len(times_list):
            val_str = str(times_list[i])
            text_w = get_text_width(val_str)
            
            start_x = slots[i]["min_x"] + (slot_width - text_w) // 2
            draw_text_custom(pixoo, val_str, start_x, y, color)

def main():
    print(f"Syncing with Pixoo 64 at IP: {PIXOO_IP}...")
    try: pixoo = Pixoo(PIXOO_IP)
    except Exception as e: print(f"Init failed: {e}"); return

    while True:
        weather, stocks, subway = get_weather(), get_stocks(), get_subway_times(STATION_ID)
        pixoo.clear()
        
        WHITE, ORANGE, VIVID_BLUE, CYAN, GREEN, RED, GRAY = (255, 255, 255), (255, 110, 0), (0, 120, 255), (0, 255, 255), (0, 255, 0), (255, 0, 0), (100, 100, 100)
        stock_color = GREEN if stocks['up'] else RED
        
        # --- WEATHER CARD ---
        now_local = datetime.now()
        days_map = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        date_str = f"{days_map[now_local.weekday()]} {now_local.month}/{now_local.day}"
        draw_text_custom(pixoo, date_str, 2, 2, WHITE)
        
        # Labels right-aligned to column 42 to ensure perfectly aligned text stacking
        draw_text_custom(pixoo, "HI", 42 - get_text_width("HI"), 8, ORANGE)
        draw_text_custom(pixoo, "LO", 42 - get_text_width("LO"), 14, VIVID_BLUE)
        
        # Small raindrop icon mini-graphic replacing "RN" label text
        raindrop = [(1,0), (1,1), (2,1), (0,2), (1,2), (2,2), (3,2), (0,3), (1,3), (2,3), (3,3), (1,4), (2,4)]
        for dx, dy in raindrop:
            pixoo.draw_pixel((38 + dx, 20 + dy), CYAN)
        
        # Values right-aligned to column 62 to preserve a clean 1-pixel right margin
        draw_text_custom(pixoo, f"{weather['curr']}F", 62 - get_text_width(f"{weather['curr']}F"), 2, WHITE)
        draw_text_custom(pixoo, f"{weather['high']}F", 62 - get_text_width(f"{weather['high']}F"), 8, ORANGE)
        draw_text_custom(pixoo, f"{weather['low']}F", 62 - get_text_width(f"{weather['low']}F"), 14, VIVID_BLUE)
        draw_text_custom(pixoo, f"{weather['rain']}%", 61 - get_text_width(f"{weather['rain']}%"), 20, CYAN)
        
        # Draw weather icon bounded within column limits
        draw_large_weather_icon(pixoo, weather['cond'], x_min=0, x_max=28, y_min=8, y_max=25)
        draw_dotted_line(pixoo, 26, GRAY)
        
        # --- STOCKS CARD ---
        draw_text_custom(pixoo, "SP500", 2, 29, stock_color)
        
        # Performance value pinned right, with trend arrow offset 6 pixels to the left
        val_x = 61 - get_text_width(stocks['perf'])
        draw_text_custom(pixoo, stocks['perf'], val_x, 29, stock_color)
        draw_text_custom(pixoo, stocks['arrow'], val_x - 6, 29, stock_color)
        
        draw_dotted_line(pixoo, 36, GRAY)
        
        # --- MTA TRANSIT CARD ---
        draw_mta_bullet(pixoo, 'A', 2, 38, VIVID_BLUE)
        draw_mta_bullet(pixoo, 'C', 10, 38, VIVID_BLUE)
        draw_mta_bullet(pixoo, 'E', 18, 38, VIVID_BLUE)
        
        draw_text_custom(pixoo, "UP", 2, 47, VIVID_BLUE)
        draw_stationary_train_times(pixoo, subway['uptown'], 47, WHITE)
        
        draw_text_custom(pixoo, "DOWN", 2, 55, VIVID_BLUE)
        draw_stationary_train_times(pixoo, subway['downtown'], 55, WHITE)
        
        try: pixoo.push()
        except Exception as e: print(f"Push failed: {e}")
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    main()