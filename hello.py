
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Create a ChromeOptions object
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


# Set the path to the ChromeDriver executable
chrome_options.add_argument('path/to/chromedriver')

# Create a new ChromeDriver instance with the options
driver = webdriver.Chrome(options=chrome_options)

# Initialize an empty dictionary to store the menu data
menu_data = {}

# Loop to get menus for multiple weeks
for week in range(0, 3):  # Get data for week 0 (first week), 1, and 2
    url = 'https://www.cbnucoop.com/service/restaurant/' if week == 0 else f'https://www.cbnucoop.com/service/restaurant/?week={week}'
    driver.get(url)
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table')
    headers = tables[0].find_all('th', {'class': 'weekday-title'})
    dates = [header.text for header in headers]
    rows = tables[0].find_all('tr')

    week_data = {}
    for row in rows[1:]:
        cols = row.find_all('td')
        for i, col in enumerate(cols):
            menu_text = col.text.strip().replace('\n', ' ').replace('\r', '')
            week_data[dates[i]] = menu_text

    menu_data[f"Week {week + 1}"] = week_data  # Week numbering starts from 1

driver.quit()

# Convert the Python dictionary to a JSON string
menu_data_json = json.dumps(menu_data)

# Generate HTML with the collected menu data
with open('index.html', 'w', encoding='utf-8') as f:
    f.write('<html>\n<head>\n<meta charset="UTF-8">\n<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="style.css">\n<title>Menu</title>\n')
    f.write(
        f'<script src="script.js"></script>\n<script>\nlet menuData = {menu_data_json};\n</script>\n')
    f.write('</head>\n<body>\n<h1>충북대학교 한빛식당 학식</h1>\n<button onclick="showMenu(\'Week 1\')">Week 1</button>\n<button onclick="showMenu(\'Week 2\')">Week 2</button>\n<button onclick="showMenu(\'Week 3\')">Week 3</button>\n<table id="menuTable">\n<!-- Menu data will be inserted here -->\n</table>\n</body>\n</html>')

# Done
print("Done collecting and generating menu data!")
