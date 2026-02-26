/**
 * chart.js — Responsabilidad única: renderizado del gráfico de población por región.
 */

const CHART_COLORS = [
  "#6366f1", "#10b981", "#f59e0b", "#ef4444",
  "#3b82f6", "#8b5cf6", "#ec4899", "#14b8a6",
  "#f97316", "#84cc16",
];

let chartInstance = null;

/**
 * Agrupa la población total por región y renderiza el gráfico de barras.
 * Destruye el gráfico anterior si existe.
 * @param {Array} countries
 */
export function renderChart(countries) {
  const regionTotals = aggregateByRegion(countries);
  const entries = Object.entries(regionTotals).sort(([, a], [, b]) => b - a);

  const labels = entries.map(([region]) => region);
  const data = entries.map(([, total]) => total);

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(document.getElementById("chart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Población total",
        data,
        backgroundColor: CHART_COLORS.slice(0, labels.length),
        borderRadius: 6,
      }],
    },
    options: buildChartOptions(),
  });
}

/**
 * Reduce la lista de países a un mapa { región: poblaciónTotal }.
 * @param {Array} countries
 * @returns {Object}
 */
function aggregateByRegion(countries) {
  return countries.reduce((acc, c) => {
    if (!c.region || c.population == null) return acc;
    acc[c.region] = (acc[c.region] ?? 0) + c.population;
    return acc;
  }, {});
}

/**
 * Retorna la configuración de opciones del gráfico.
 * @returns {Object}
 */
function buildChartOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (ctx) => ` ${ctx.parsed.y.toLocaleString("es-AR")} hab.`,
        },
      },
    },
    scales: {
      y: {
        ticks: {
          callback: (v) => {
            if (v >= 1e9) return (v / 1e9).toFixed(1) + "B";
            if (v >= 1e6) return (v / 1e6).toFixed(0) + "M";
            return v;
          },
        },
      },
    },
  };
}
