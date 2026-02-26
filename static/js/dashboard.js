/**
 * dashboard.js — Orquestador principal.
 * Responsabilidad: inicializar la app, escuchar eventos del DOM
 * y coordinar los módulos api, table, chart y ui.
 */

import { syncCountries, fetchRegions, fetchCountries } from "./api.js";
import { renderTable, sortCountries, applySorting } from "./table.js";
import { renderChart } from "./chart.js";
import { showToast, updateStats, updateRegionCount } from "./ui.js";

// ── Estado de la aplicación ──
let allCountries = [];

// ── Inicialización ──
window.addEventListener("DOMContentLoaded", async () => {
  bindEvents();
  await loadRegions();
  await loadCountries();
});

// ── Binding de eventos ──
function bindEvents() {
  document.getElementById("syncBtn").addEventListener("click", handleSync);
  document.getElementById("searchInput").addEventListener("input", loadCountries);
  document.getElementById("regionSelect").addEventListener("change", loadCountries);

  document.querySelectorAll("[data-sort]").forEach((th) => {
    th.addEventListener("click", () => {
      allCountries = sortCountries(allCountries, th.dataset.sort);
      renderTable(allCountries);
    });
  });
}

// ── Handlers ──

async function handleSync() {
  const btn = document.getElementById("syncBtn");
  btn.disabled = true;
  btn.innerHTML = '<span class="animate-spin inline-block">🔄</span> Sincronizando...';

  try {
    const result = await syncCountries();
    showToast(result.message, "green");
    await loadRegions();
    await loadCountries();
  } catch (err) {
    showToast("Error al sincronizar: " + err.message, "red");
  } finally {
    btn.disabled = false;
    btn.innerHTML = "<span>🔄</span> Sincronizar datos";
  }
}

async function loadRegions() {
  try {
    const regions = await fetchRegions();
    populateRegionSelect(regions);
    updateRegionCount(regions.length);
  } catch (_) {
    // Si no hay datos aún, el select queda vacío silenciosamente
  }
}

async function loadCountries() {
  const search = document.getElementById("searchInput").value.trim();
  const region = document.getElementById("regionSelect").value;

  try {
    allCountries = await fetchCountries({ search, region });
    allCountries = applySorting(allCountries);
    renderTable(allCountries);
    renderChart(allCountries);
    updateStats(allCountries);
  } catch (err) {
    showToast("Error al cargar datos.", "red");
  }
}

// ── Helpers de DOM ──

function populateRegionSelect(regions) {
  const select = document.getElementById("regionSelect");
  const currentValue = select.value;

  select.innerHTML = '<option value="">Todas las regiones</option>';
  regions.forEach((region) => {
    const opt = document.createElement("option");
    opt.value = region;
    opt.textContent = region;
    select.appendChild(opt);
  });

  // Restaurar selección previa si sigue siendo válida
  if (currentValue && regions.includes(currentValue)) {
    select.value = currentValue;
  }
}
