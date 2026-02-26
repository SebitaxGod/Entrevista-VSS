/**
 * api.js — Responsabilidad única: todas las llamadas HTTP a la API.
 */

const BASE_URL = "";

export async function syncCountries() {
  const res = await fetch(`${BASE_URL}/api/countries/sync`, { method: "POST" });
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function fetchRegions() {
  const res = await fetch(`${BASE_URL}/api/countries/regions`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function fetchCountries({ search = "", region = "", limit = 250 } = {}) {
  const params = new URLSearchParams({ limit });
  if (search) params.set("search", search);
  if (region) params.set("region", region);

  const res = await fetch(`${BASE_URL}/api/countries/?${params}`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}
