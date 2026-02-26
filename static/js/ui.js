/**
 * ui.js — Responsabilidad única: manipulación de la UI (toast, stats, formato).
 */

/**
 * Muestra un mensaje temporal en la esquina superior derecha.
 * @param {string} msg
 * @param {"green"|"red"|"blue"} color
 */
export function showToast(msg, color) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.className = `fixed top-4 right-4 z-50 px-5 py-3 rounded-lg shadow-lg text-white text-sm font-medium bg-${color}-600`;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 4000);
}

/**
 * Actualiza las tarjetas de estadísticas con los datos actuales.
 * @param {Array} countries
 */
export function updateStats(countries) {
  const total = countries.length;
  const totalPop = countries.reduce((sum, c) => sum + (c.population ?? 0), 0);
  const maxCountry = countries.reduce(
    (best, c) => (!best || (c.population ?? 0) > (best.population ?? 0)) ? c : best,
    null
  );

  document.getElementById("statTotal").textContent = total || "—";
  document.getElementById("statPop").textContent = total ? formatBig(totalPop) : "—";
  document.getElementById("statMax").textContent = maxCountry ? maxCountry.name : "—";
}

/**
 * Actualiza el contador de regiones en la tarjeta de stats.
 * @param {number} count
 */
export function updateRegionCount(count) {
  document.getElementById("statRegions").textContent = count || "—";
}

/**
 * Formatea un número grande en notación compacta (B / M).
 * @param {number} n
 * @returns {string}
 */
export function formatBig(n) {
  if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(1) + "M";
  return n.toLocaleString("es-AR");
}
