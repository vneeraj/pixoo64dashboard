import time
import math
import requests
import yfinance as yf
from datetime import datetime
from pixoo import Pixoo

# ==================== CONFIGURATION ====================
PIXOO_IP = "192.168.1.153"  # Replace with your Pixoo 64's local IP address
STATION_ID = "A28"          # "A28" is 34 St-Penn Station (A/C/E). Change to your target station ID.
MIN_CATCHABLE_MIN = 6       # Ignore trains closer than this (walking time to station). Fallback shows soonest if empty.
REFRESH_INTERVAL = 30       # Time in seconds between background data refreshes

# --- TICKER SPEED CONTROLS (BLOOMBERG-STYLE) ---
TICKER_SPEED = 0.02         # Lower value = faster refresh rate (seconds per frame shift)
TICKER_STEP = 1             # Pixels shifted per frame. Keep at 1 for max smoothness.
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
    w_map = {'M':5, 'N':5, 'W':5, 'Q':5, 'I':3, 'T':3, 'Y':3, '1':3, '.':1, ' ':2, '%':3, '/':3, '▲':3, '▼':3}
    return sum(w_map.get(c, 4) + 1 for c in text) - 1

def draw_text_custom(pixoo, text, start_x, start_y, color):
    w_map = {'M':5, 'N':5, 'W':5, 'Q':5, 'I':3, 'T':3, 'Y':3, '1':3, '.':1, ' ':2, '%':3, '/':3, '▲':3, '▼':3}
    current_x = start_x
    for char in text:
        if char in CUSTOM_FONT:
            for dx, dy in CUSTOM_FONT[char]:
                px = current_x + dx
                py = start_y + dy
                if 0 <= px < 64 and 0 <= py < 64:
                    pixoo.draw_pixel((px, py), color)
            current_x += w_map.get(char, 4) + 1

# --- DATA ACQUISITION MODULES ---
def get_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=40.7539&longitude=-74.0010&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min,sunset&hourly=precipitation_probability&temperature_unit=fahrenheit&timezone=America%2FNew_York&forecast_days=1"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        
        curr = str(int(round(data['current']['temperature_2m'])))
        high = str(int(round(data['daily']['temperature_2m_max'][0])))
        low = str(int(round(data['daily']['temperature_2m_min'][0])))
        
        current_hour = datetime.now().hour
        remaining_probs = data['hourly']['precipitation_probability'][current_hour:]
        rain = str(max(remaining_probs)) if remaining_probs else "0"
        wmo_code = data['current']['weather_code']
        
        if wmo_code in [0]: cond = "clear"
        elif wmo_code in [1, 2]: cond = "partly cloudy"
        elif wmo_code in [3, 45, 48]: cond = "cloudy"
        elif wmo_code in [71, 73, 75, 77, 85, 86]: cond = "snow"
        else: cond = "rain"
            
        sunset_raw = data['daily']['sunset'][0]
        sunset_dt = datetime.strptime(sunset_raw, "%Y-%m-%dT%H:%M")
        is_night = datetime.now() >= sunset_dt
        
        hour_12 = sunset_dt.hour % 12
        if hour_12 == 0: hour_12 = 12
        sunset_str = f"{hour_12}:{sunset_dt.minute:02d}P"
            
        return {"curr": curr, "high": high, "low": low, "rain": rain, "cond": cond, "sunset": sunset_str, "is_night": is_night}
    except Exception as e:
        print(f"Hudson Yards Weather Fetch Error: {e}")
        return {"curr": "--", "high": "--", "low": "--", "rain": "--", "cond": "unknown", "sunset": "--:--P", "is_night": False}

def get_financials():
    GREEN, RED, WHITE = (0, 255, 0), (255, 0, 0), (255, 255, 255)
    res = {
        "spx": {"perf": "--%", "arrow": "▲", "color": GREEN},
        "rut": {"perf": "--%", "arrow": "▲", "color": GREEN},
        "tnx": {"perf": "--%", "color": WHITE}
    }
    try:
        tickers = yf.Tickers("^GSPC ^RUT ^TNX")
        
        h_spx = tickers.tickers["^GSPC"].history(period="2d")
        if len(h_spx) >= 2:
            pct = ((h_spx['Close'].iloc[-1] - h_spx['Close'].iloc[-2]) / h_spx['Close'].iloc[-2]) * 100
            res["spx"] = {"perf": f"{abs(pct):.2f}%", "arrow": "▲" if pct >= 0 else "▼", "color": GREEN if pct >= 0 else RED}
            
        h_rut = tickers.tickers["^RUT"].history(period="2d")
        if len(h_rut) >= 2:
            pct = ((h_rut['Close'].iloc[-1] - h_rut['Close'].iloc[-2]) / h_rut['Close'].iloc[-2]) * 100
            res["rut"] = {"perf": f"{abs(pct):.2f}%", "arrow": "▲" if pct >= 0 else "▼", "color": GREEN if pct >= 0 else RED}
            
        h_tnx = tickers.tickers["^TNX"].history(period="1d")
        if len(h_tnx) >= 1:
            val = h_tnx['Close'].iloc[-1]
            res["tnx"] = {"perf": f"{val:.2f}%", "color": WHITE}
    except Exception as e:
        print(f"Financial Market Fetch Error: {e}")
    return res

def get_moon_phase_value():
    now = datetime.now()
    diff = now - datetime(2000, 1, 6, 18, 14)
    return (diff.total_seconds() / 86400.0 % 29.530588853) / 29.530588853

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
        uptown_times = sorted(list(set(uptown_times)))
        downtown_times = sorted(list(set(downtown_times)))

        catchable_uptown = [t for t in uptown_times if t >= MIN_CATCHABLE_MIN][:3]
        catchable_downtown = [t for t in downtown_times if t >= MIN_CATCHABLE_MIN][:3]

        # Fallback: if nothing is catchable, show soonest trains anyway so the row
        # doesn't read as "no data" when trains are just too close to make.
        if not catchable_uptown:
            catchable_uptown = uptown_times[:3]
        if not catchable_downtown:
            catchable_downtown = downtown_times[:3]

        uptown_times = catchable_uptown
        downtown_times = catchable_downtown
    except Exception as e:
        print(f"MTA Subway Fetch Error: {e}")
    return {"uptown": uptown_times, "downtown": downtown_times}

# --- GRAPHICS ENGINE MODULES ---
def draw_dotted_line(pixoo, y, color):
    for x in range(0, 64, 2):
        pixoo.draw_pixel((x, y), color)

def draw_large_moon_phase(pixoo, phase_val, x_min=0, x_max=28, y_min=9, y_max=26):
    cx = x_min + (x_max - x_min + 1) // 2
    cy = y_min + (y_max - y_min + 1) // 2
    R = 7.2
    phi = math.pi - (2.0 * math.pi * phase_val)
    
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            dx, dy = x - cx, y - cy
            dist_sq = dx * dx + dy * dy
            
            if dist_sq <= R * R:
                nx = max(-1.0, min(1.0, dx / R))
                ny = max(-1.0, min(1.0, dy / R))
                alpha = math.asin(nx)
                
                lighting = math.cos(alpha - phi)
                z = math.sqrt(max(0.0, 1.0 - nx * nx - ny * ny))
                
                if lighting > 0:
                    if lighting > 0.6 and z > 0.4: col = (255, 255, 255)
                    elif lighting > 0.2: col = (240, 240, 225)
                    else: col = (180, 185, 195)
                    
                    is_crater = False
                    craters = [(-2, -2, 1.8), (3, 1, 1.4), (-1, 3, 1.9)]
                    for cxr, cyr, crad in craters:
                        if (dx - cxr)**2 + (dy - cyr)**2 <= crad**2:
                            is_crater = True
                            break
                    if is_crater:
                        col = (int(col[0] * 0.62), int(col[1] * 0.62), int(col[2] * 0.65))
                else:
                    glow = int(14 + (1.0 - z) * 14)
                    col = (glow, glow + 4, glow + 14)
                    
                pixoo.draw_pixel((x, y), col)

def draw_large_weather_icon(pixoo, condition, x_min=0, x_max=28, y_min=9, y_max=26):
    SUN_WHITE, SUN_CORE, SUN_GLOW, SUN_RAY = (255, 255, 230), (255, 230, 0), (255, 120, 0), (230, 60, 0)
    CLOUD_WHITE, CLOUD_BODY, CLOUD_SHADE = (255, 255, 255), (185, 195, 205), (105, 115, 125)
    STORM_BODY, STORM_SHADE = (110, 115, 125), (65, 70, 80)
    RAIN_DEEP, RAIN_LITE, SNOW_CRYST = (0, 95, 230), (75, 175, 255), (215, 240, 255)
    
    pixels = []
    if condition == "rain":
        for dx in range(2, 16):
            for dy in range(3, 9): pixels.append((dx, dy, STORM_BODY))
        for dx in range(5, 13):
            for dy in range(1, 3): pixels.append((dx, dy, STORM_BODY))
        for dx in range(2, 16): pixels.append((dx, 8, STORM_SHADE))
        pixels.extend([
            (4, 10, RAIN_LITE), (3, 11, RAIN_DEEP), (2, 12, RAIN_DEEP),
            (8, 10, RAIN_LITE), (7, 11, RAIN_DEEP), (6, 12, RAIN_DEEP),
            (12, 10, RAIN_LITE), (11, 11, RAIN_DEEP), (10, 12, RAIN_DEEP),
            (15, 10, RAIN_LITE), (14, 11, RAIN_DEEP), (13, 12, RAIN_DEEP)
        ])
    elif condition == "snow":
        for dx in range(2, 16):
            for dy in range(3, 9): pixels.append((dx, dy, CLOUD_BODY))
        for dx in range(5, 13):
            for dy in range(1, 3): pixels.append((dx, dy, CLOUD_WHITE))
        for dx in range(2, 16): pixels.append((dx, 8, CLOUD_SHADE))
        pixels.extend([
            (4, 10, CLOUD_WHITE), (3, 11, SNOW_CRYST), (5, 11, SNOW_CRYST), (4, 12, CLOUD_WHITE),
            (9, 11, CLOUD_WHITE), (8, 12, SNOW_CRYST), (10, 12, SNOW_CRYST), (9, 13, CLOUD_WHITE),
            (14, 10, CLOUD_WHITE), (13, 11, SNOW_CRYST), (15, 11, SNOW_CRYST), (14, 12, CLOUD_WHITE)
        ])
    elif condition == "cloudy":
        for dx in range(1, 17):
            for dy in range(4, 11): pixels.append((dx, dy, CLOUD_BODY))
        for dx in range(4, 14):
            for dy in range(1, 4): pixels.append((dx, dy, CLOUD_BODY))
        top_highlights = [(4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1), (1,4), (2,4), (3,4), (14,4), (15,4), (16,4)]
        for dx, dy in top_highlights: pixels.append((dx, dy, CLOUD_WHITE))
        for dx in range(1, 17): pixels.append((dx, 10, CLOUD_SHADE))
    elif condition == "partly cloudy":
        for dx in range(1, 10):
            for dy in range(1, 10): pixels.append((dx, dy, SUN_GLOW))
        for dx in range(2, 9):
            for dy in range(2, 9): pixels.append((dx, dy, SUN_CORE))
        for dx in range(4, 7):
            for dy in range(4, 7): pixels.append((dx, dy, SUN_WHITE))
        for dx in range(6, 19):
            for dy in range(6, 13): pixels.append((dx, dy, CLOUD_BODY))
        for dx in range(9, 16):
            for dy in range(4, 6): pixels.append((dx, dy, CLOUD_BODY))
        top_rim = [(9,3), (10,3), (11,3), (12,3), (13,3), (14,3), (15,3), (6,5), (7,5), (8,5), (16,5), (17,5), (18,5)]
        for dx, dy in top_rim: pixels.append((dx, dy, CLOUD_WHITE))
        for dx in range(6, 19): pixels.append((dx, 12, CLOUD_SHADE))
    else:
        for dx in range(3, 12):
            for dy in range(3, 12): pixels.append((dx, dy, SUN_GLOW))
        for dx in range(4, 11):
            for dy in range(4, 11): pixels.append((dx, dy, SUN_CORE))
        for dx in range(6, 9):
            for dy in range(6, 9): pixels.append((dx, dy, SUN_WHITE))
        rays_glow = [(7,0), (7,14), (0,7), (14,7), (2,2), (12,2), (2,12), (12,12)]
        rays_fire = [(7,1), (7,13), (1,7), (13,7), (3,3), (11,3), (3,11), (11,11), (7,2), (7,12), (2,7), (12,7)]
        for dx, dy in rays_glow: pixels.append((dx, dy, SUN_GLOW))
        for dx, dy in rays_fire: pixels.append((dx, dy, SUN_RAY))
        
    all_dx, all_dy = [p[0] for p in pixels], [p[1] for p in pixels]
    icon_w, icon_h = max(all_dx) - min(all_dx) + 1, max(all_dy) - min(all_dy) + 1
    box_w, box_h = x_max - x_min + 1, y_max - y_min + 1
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
    slots = [{"min_x": 29, "max_x": 37}, {"min_x": 41, "max_x": 49}, {"min_x": 53, "max_x": 61}]
    slot_width = 9
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

def draw_mini_sunset(pixoo, x, y):
    YELLOW, ORANGE, DEEP_BLUE = (255, 220, 0), (255, 90, 0), (0, 70, 190)
    for dx, dy in [(2,1), (3,1), (4,1), (1,2), (2,2), (3,2), (4,2), (5,2)]:
        if 0 <= x + dx < 64: pixoo.draw_pixel((x + dx, y + dy), YELLOW)
    if 0 <= x + 3 < 64: pixoo.draw_pixel((x + 3, y), ORANGE)
    for dx in range(0, 7):
        if 0 <= x + dx < 64: pixoo.draw_pixel((x + dx, y + 3), DEEP_BLUE)

def main():
    print(f"Syncing with Pixoo 64 at IP: {PIXOO_IP}...")
    try: pixoo = Pixoo(PIXOO_IP)
    except Exception as e: print(f"Init failed: {e}"); return

    last_fetch_time = 0
    weather, financials, subway = None, None, None
    ticker_x = 64

    while True:
        current_time = time.time()
        if current_time - last_fetch_time >= REFRESH_INTERVAL or weather is None:
            weather = get_weather()
            financials = get_financials()
            subway = get_subway_times(STATION_ID)
            last_fetch_time = current_time

        pixoo.clear()
        WHITE, ORANGE, VIVID_BLUE, CYAN, GRAY = (255, 255, 255), (255, 110, 0), (0, 120, 255), (0, 255, 255), (80, 80, 80)
        
        # --- WEATHER CARD ---
        now_local = datetime.now()
        days_map = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        date_str = f"{days_map[now_local.weekday()]} {now_local.month}/{now_local.day}"
        draw_text_custom(pixoo, date_str, 2, 3, WHITE)
        
        draw_text_custom(pixoo, "HI", 42 - get_text_width("HI"), 9, ORANGE)
        draw_text_custom(pixoo, "LO", 42 - get_text_width("LO"), 15, VIVID_BLUE)
        
        if weather['cond'] == "snow":
            snowflake = [(0,0), (3,0), (1,1), (2,1), (0,2), (1,2), (2,2), (3,2), (1,3), (2,3), (0,4), (3,4)]
            for dx, dy in snowflake: pixoo.draw_pixel((38 + dx, 21 + dy), WHITE)
        else:
            raindrop = [(1,0), (1,1), (2,1), (0,2), (1,2), (2,2), (3,2), (0,3), (1,3), (2,3), (3,3), (1,4), (2,4)]
            for dx, dy in raindrop: pixoo.draw_pixel((38 + dx, 21 + dy), CYAN)
        
        draw_text_custom(pixoo, f"{weather['curr']}F", 62 - get_text_width(f"{weather['curr']}F"), 3, WHITE)
        draw_text_custom(pixoo, f"{weather['high']}F", 62 - get_text_width(f"{weather['high']}F"), 9, ORANGE)
        draw_text_custom(pixoo, f"{weather['low']}F", 62 - get_text_width(f"{weather['low']}F"), 15, VIVID_BLUE)
        draw_text_custom(pixoo, f"{weather['rain']}%", 61 - get_text_width(f"{weather['rain']}%"), 21, CYAN)
        
        if weather.get('is_night', False) and weather['cond'] not in ["rain", "snow"]:
            current_phase_val = get_moon_phase_value()
            draw_large_moon_phase(pixoo, current_phase_val, x_min=0, x_max=28, y_min=9, y_max=26)
        else:
            draw_large_weather_icon(pixoo, weather['cond'], x_min=0, x_max=28, y_min=9, y_max=26)
            
        draw_dotted_line(pixoo, 27, GRAY)
        
        # --- DOUBLE-BUFFERED SEAMLESS TICKER ---
        ticker_items = [
            ('text', f"SPX {financials['spx']['arrow']}{financials['spx']['perf']}", financials['spx']['color']),
            ('space', 14, None),
            ('text', f"RUT {financials['rut']['arrow']}{financials['rut']['perf']}", financials['rut']['color']),
            ('space', 14, None),
            ('text', f"TNX {financials['tnx']['perf']}", financials['tnx']['color']),
            ('space', 14, None),
            ('icon', 'sunset', None),
            ('space', 3, None),
            ('text', weather['sunset'], ORANGE),
            ('space', 14, None)  # Synchronized with standard 14px interval for seamless looping
        ]
        
        total_ticker_width = 0
        for itype, val, _ in ticker_items:
            if itype == 'text': total_ticker_width += get_text_width(val)
            elif itype == 'space': total_ticker_width += val
            elif itype == 'icon': total_ticker_width += 7

        for loop_offset in [0, total_ticker_width]:
            cx = ticker_x + loop_offset
            for itype, val, col in ticker_items:
                if itype == 'text': item_w = get_text_width(val)
                elif itype == 'space': item_w = val
                elif itype == 'icon': item_w = 7
                
                if -item_w <= cx < 64:
                    if itype == 'text':
                        draw_text_custom(pixoo, val, cx, 30, col)
                    elif itype == 'icon' and val == 'sunset':
                        draw_mini_sunset(pixoo, cx, 31)
                cx += item_w

        ticker_x -= TICKER_STEP
        if ticker_x <= -total_ticker_width:
            ticker_x = 0

        draw_dotted_line(pixoo, 37, GRAY)
        
        # --- MTA TRANSIT CARD ---
        draw_mta_bullet(pixoo, 'A', 2, 39, VIVID_BLUE)
        draw_mta_bullet(pixoo, 'C', 12, 39, VIVID_BLUE)
        draw_mta_bullet(pixoo, 'E', 22, 39, VIVID_BLUE)
        
        draw_text_custom(pixoo, "UP", 2, 48, VIVID_BLUE)
        draw_stationary_train_times(pixoo, subway['uptown'], 48, WHITE)
        
        draw_text_custom(pixoo, "DOWN", 2, 56, VIVID_BLUE)
        draw_stationary_train_times(pixoo, subway['downtown'], 56, WHITE)
        
        try: pixoo.push()
        except Exception as e: print(f"Push failed: {e}")
        time.sleep(TICKER_SPEED)

if __name__ == "__main__":
    main()
