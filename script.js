function showMenu(week) {
  let menu = menuData[week];
  let tableContent = "";
  for (let [date, menuItem] of Object.entries(menu)) {
    tableContent += `<tr><td>${date}</td><td>${menuItem}</td></tr>`;
  }
  document.getElementById("menuTable").innerHTML = tableContent;
}

// 페이지가 로드되면 기본적으로 "Week 1"의 메뉴를 표시
window.onload = function () {
  showMenu("Week 1");
};
