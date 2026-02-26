/**
 * table.js — Responsabilidad única: renderizado y ordenamiento de la tabla de países.
 */

let sortKey = "name";
let sortAsc = true;

/**
 * Ordena los países por la clave dada, alternando asc/desc si se repite.
 * @param {Array} countries
 * @param {string} key
 * @returns {Array}
 */
export function sortCountries(countries, key) {
  if (sortKey === key) {
    sortAsc = !sortAsc;
  } else {
    sortKey = key;
    sortAsc = true;
  }
  return applySorting(countries);
}

/**
 * Aplica el ordenamiento actual sin cambiar la clave.
 * @param {Array} countries
 * @returns {Array}
 */
export function applySorting(countries) {
  return [...countries].sort((a, b) => {
    let va = a[sortKey] ?? "";
    let vb = b[sortKey] ?? "";
    if (typeof va === "string") va = va.toLowerCase();
    if (typeof vb === "string") vb = vb.toLowerCase();
    return sortAsc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
  });
}

/**
 * Renderiza la tabla con la lista de países provista.
 * @param {Array} countries
 */
export function renderTable(countries) {
  const tbody = document.getElementById("tableBody");
  const rowCount = document.getElementById("rowCount");

  tbody.replaceChildren();

  if (!countries.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 7;
    td.className = "text-center py-10 text-gray-400";
    td.textContent = "Sin resultados.";
    tr.appendChild(td);
    tbody.appendChild(tr);
    rowCount.textContent = "";
    return;
  }

  rowCount.textContent = `${countries.length} países`;
  const fragment = document.createDocumentFragment();
  countries.forEach((country) => fragment.appendChild(buildRow(country)));
  tbody.appendChild(fragment);
}

/**
 * Crea un elemento td con las clases y contenido dados.
 * @param {string} className
 * @param {string|Node} content
 * @returns {HTMLTableCellElement}
 */
function createCell(className, content) {
  const td = document.createElement("td");
  td.className = className;
  if (content instanceof Node) {
    td.appendChild(content);
  } else {
    td.textContent = content;
  }
  return td;
}

/**
 * Construye un elemento <tr> para un país usando el DOM API.
 * @param {Object} country
 * @returns {HTMLTableRowElement}
 */
function buildRow(country) {
  const tr = document.createElement("tr");
  tr.className = "hover:bg-indigo-50 transition-colors";

  // Bandera
  const flagTd = document.createElement("td");
  flagTd.className = "px-4 py-2";
  if (country.flag_url) {
    const img = document.createElement("img");
    img.src = country.flag_url;
    img.alt = country.name;
    img.className = "w-8 h-5 object-cover rounded shadow-sm";
    flagTd.appendChild(img);
  } else {
    flagTd.textContent = "—";
  }

  // Nombre
  const nameTd = createCell("px-4 py-2 font-medium", country.name);

  // Capital
  const capitalTd = createCell("px-4 py-2 text-gray-500", country.capital ?? "—");

  // Región (con badge)
  const regionTd = document.createElement("td");
  regionTd.className = "px-4 py-2";
  const badge = document.createElement("span");
  badge.className = "inline-block bg-indigo-100 text-indigo-700 text-xs px-2 py-0.5 rounded-full";
  badge.textContent = country.region ?? "—";
  regionTd.appendChild(badge);

  // Subregión
  const subregionTd = createCell("px-4 py-2 text-gray-500 text-xs", country.subregion ?? "—");

  // Población
  const population = country.population != null
    ? country.population.toLocaleString("es-AR")
    : "—";
  const populationTd = createCell("px-4 py-2 text-right tabular-nums", population);

  // Área
  const area = country.area != null
    ? country.area.toLocaleString("es-AR", { maximumFractionDigits: 0 })
    : "—";
  const areaTd = createCell("px-4 py-2 text-right tabular-nums", area);

  tr.append(flagTd, nameTd, capitalTd, regionTd, subregionTd, populationTd, areaTd);
  return tr;
}
