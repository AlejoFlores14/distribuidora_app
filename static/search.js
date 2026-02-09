document.getElementById("searchInput").addEventListener("input", function () {
  let filter = this.value.toLowerCase();
  let rows = document.querySelectorAll("#productsTable tbody tr");

  rows.forEach(row => {
    let codigo = row.querySelector(".codigo");
    let nombre = row.querySelector(".nombre");

    let codigoText = codigo.textContent.toLowerCase();
    let nombreText = nombre.textContent.toLowerCase();

    codigo.innerHTML = codigo.textContent;
    nombre.innerHTML = nombre.textContent;

    if (codigoText.includes(filter) || nombreText.includes(filter)) {
      row.style.display = "";
      highlight(codigo, filter);
      highlight(nombre, filter);
    } else {
      row.style.display = "none";
    }
  });
});

function highlight(element, text) {
  if (!text) return;
  let regex = new RegExp(`(${text})`, "gi");
  element.innerHTML = element.textContent.replace(regex, "<mark>$1</mark>");
}