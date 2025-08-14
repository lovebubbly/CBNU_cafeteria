let currentCafeteria = "한빛식당";

function showMenu(week) {
  const menu = (menuData[currentCafeteria] || {})[week] || {};
  let tableContent = "";
  for (const [date, item] of Object.entries(menu)) {
    tableContent += `<tr><td>${date}</td><td>${item}</td></tr>`;
  }
  document.getElementById("menuTable").innerHTML = tableContent;
}

function changeCafeteria() {
  currentCafeteria = document.getElementById("cafeteriaSelect").value;
  showMenu("Week 1");
}

window.onload = function () {
  changeCafeteria();
};

