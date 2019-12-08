import curses
import os

from weather.service import OpenWeather


def get_weather(zip):
    weather_client = OpenWeather(api_key=os.environ['WEATHER_API_KEY'])
    current_weather = weather_client.get_current(zip=zip, units='imperial')
    current_forecast = weather_client.get_forecast(zip=zip, units='imperial')
    
    current_weather_str = f"current temp {current_weather['main']['temp']} F"
    current_forecast_str = "\n".join(
        [f"{item['dt_txt']} {item['main']['temp']} F" for item in current_forecast['list']]
    )

    return current_weather_str, current_forecast_str


# curses talk, inspiration: https://www.youtube.com/watch?v=eN1eZtjLEnU
# curses setup 
stdscr = curses.initscr()

curses.cbreak()
curses.curs_set(0)

if curses.has_colors():
    curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

# begin program
stdscr.addstr("Enter zipcode to get current weather and forecast. Type q to exit.", curses.A_REVERSE)
stdscr.chgat(-1, curses.A_REVERSE)
stdscr.chgat(0, 6, 7, curses.A_BOLD | curses.color_pair(1))
stdscr.chgat(0, 56, 1, curses.A_BOLD | curses.color_pair(1))

weather_window = curses.newwin(curses.LINES-1, curses.COLS, 1, 0)
weather_window.box()

weather_report_window = weather_window.subwin(curses.LINES-8, curses.COLS-4, 3, 2)
weather_report_window.addstr("enter zipcode below")

weather_zip_window = weather_window.subwin(curses.LINES-3, 2)
weather_zip_window.box()
weather_zip_window.addstr(1, 1, "zipcode:")

# update internal window data structures
stdscr.noutrefresh()
weather_window.noutrefresh()
weather_zip_window.noutrefresh()

curses.doupdate()

try:
    # event loop
    while True:

        ch = weather_zip_window.getstr(1, 12).decode()

        if ch == 'q':
            break

        weather = get_weather(ch)

        weather_report_window.refresh()
        weather_report_window.clear()
        weather_report_window.addstr(weather[0])
        weather_report_window.addstr(2, 1, weather[1])

        weather_zip_window.clear()
        weather_zip_window.box()
        weather_zip_window.addstr(1, 1, "zipcode:")

        stdscr.noutrefresh()
        weather_window.noutrefresh()
        weather_report_window.noutrefresh()
        weather_zip_window.noutrefresh()
        curses.doupdate()

finally:
    # cleanup no matter what
    curses.nocbreak()
    curses.curs_set(1)

    curses.endwin()
