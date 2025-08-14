import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# Endpoints for each cafeteria on cbnucoop.com
cafeteria_urls = {
    "한빛식당": "https://www.cbnucoop.com/service/restaurant/",
    "별빛식당": "https://www.cbnucoop.com/service/restaurant2/",
    "은하수식당": "https://www.cbnucoop.com/service/restaurant3/",
}


def fetch_menu(driver, base_url):
    """Collect three weeks of menu data starting from the current week."""
    data = {}
    for week in range(3):
        url = base_url if week == 0 else f"{base_url}?week={week}"
        driver.get(url)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        tables = soup.find_all("table")
        if not tables:
            data[f"Week {week + 1}"] = {}
            continue

        headers = tables[0].find_all("th", {"class": "weekday-title"})
        dates = [h.text for h in headers]
        rows = tables[0].find_all("tr")

        week_data = {}
        for row in rows[1:]:
            cols = row.find_all("td")
            for i, col in enumerate(cols):
                text = col.text.strip().replace("\n", " ").replace("\r", "")
                week_data[dates[i]] = text

        data[f"Week {week + 1}"] = week_data

    return data


def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    menu_data = {}
    for cafeteria, base_url in cafeteria_urls.items():
        menu_data[cafeteria] = fetch_menu(driver, base_url)

    driver.quit()

    # Save JSON data separately for reference
    with open("menu.json", "w", encoding="utf-8") as f:
        json.dump(menu_data, f, ensure_ascii=False, indent=2)

    menu_json = json.dumps(menu_data, ensure_ascii=False)

    html = f"""
<html>
<head>
<meta charset=\"UTF-8\">
<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
<link href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;500&display=swap\" rel=\"stylesheet\">
<link rel=\"stylesheet\" href=\"style.css\">
<title>Menu</title>
<script src=\"script.js\"></script>
<script>
let menuData = {menu_json};
</script>
</head>
<body>
<h1>충북대학교 학식</h1>
<select id=\"cafeteriaSelect\" onchange=\"changeCafeteria()\">
  <option value=\"한빛식당\">한빛식당</option>
  <option value=\"별빛식당\">별빛식당</option>
  <option value=\"은하수식당\">은하수식당</option>
</select>
<div id=\"weekButtons\">
  <button onclick=\"showMenu('Week 1')\">Week 1</button>
  <button onclick=\"showMenu('Week 2')\">Week 2</button>
  <button onclick=\"showMenu('Week 3')\">Week 3</button>
</div>
<table id=\"menuTable\"></table>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    main()

