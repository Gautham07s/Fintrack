document.addEventListener("DOMContentLoaded", () => {
  const pieEl = document.getElementById("pieChart");
  if (pieEl) {
    const labels = JSON.parse(pieEl.dataset.labels || "[]");
    const values = JSON.parse(pieEl.dataset.values || "[]");
    new Chart(pieEl, {
      type: "doughnut",
      data: { labels, datasets: [{ data: values }] },
      options: { plugins: { legend: { position: "bottom" } }, cutout: "55%" }
    });
  }
  const lineEl = document.getElementById("lineChart");
  if (lineEl) {
    const labels = JSON.parse(lineEl.dataset.labels || "[]");
    const values = JSON.parse(lineEl.dataset.values || "[]");
    new Chart(lineEl, {
      type: "line",
      data: { labels, datasets: [{ data: values, fill: false, tension: 0.25 }] },
      options: {
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        plugins: { legend: { display: false } }
      }
    });
  }
});
