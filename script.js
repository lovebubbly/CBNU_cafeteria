function showMenu(week) {
  const menu = menuData[week];
  const container = document.getElementById("menuContainer");
  container.innerHTML = "";
  for (const [date, menuItem] of Object.entries(menu)) {
    const card = document.createElement("md-elevated-card");
    card.innerHTML = `
      <div slot="headline">${date}</div>
      <div slot="supporting-text">${menuItem}</div>
    `;
    container.appendChild(card);
  }
}

window.addEventListener("load", () => {
  const tabs = document.getElementById("weekTabs");
  const weeks = ["Week 1", "Week 2", "Week 3"];
  tabs.addEventListener("change", () => {
    const week = weeks[tabs.activeTabIndex];
    showMenu(week);
  });
  tabs.activeTabIndex = 0;
  showMenu(weeks[0]);
});
