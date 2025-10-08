const selectors = {
  efficiency: document.getElementById('hero-efficiency'),
  output: document.getElementById('hero-output'),
  downtime: document.getElementById('hero-downtime'),
  chipUtilization: document.getElementById('chip-utilization'),
  chipOee: document.getElementById('chip-oee'),
  chipThroughput: document.getElementById('chip-throughput'),
  avgDailyOutput: document.getElementById('avg-daily-output'),
  totalDowntime: document.getElementById('total-downtime'),
  scrapAmount: document.getElementById('scrap-amount'),
  perShiftOutput: document.getElementById('per-shift-output'),
  chartTag: document.getElementById('chart-tag'),
  simulateButton: document.getElementById('simulate'),
  resetButton: document.getElementById('reset'),
};

const configForm = document.getElementById('config-form');
let productionChart = null;

function normalizeNumber(value, fallback = 0) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function calculateOEE({ availability, performance, quality }) {
  const clamp = (v) => Math.max(0, Math.min(1, v));
  return clamp(availability) * clamp(performance) * clamp(quality);
}

function formatNumber(value, options = {}) {
  return new Intl.NumberFormat('pt-BR', options).format(value);
}

function formatHours(minutes) {
  const hours = minutes / 60;
  return `${formatNumber(hours, { maximumFractionDigits: 1 })} h`;
}

function formatPercentage(value) {
  return `${formatNumber(value * 100, { maximumFractionDigits: 1 })}%`;
}

function buildChart(ctx, labels, data) {
  if (productionChart) {
    productionChart.destroy();
  }

  productionChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Unidades produzidas',
          data,
          borderColor: '#38bdf8',
          backgroundColor: 'rgba(56, 189, 248, 0.18)',
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointBackgroundColor: '#0ea5e9',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          ticks: {
            color: 'rgba(248, 250, 252, 0.65)',
          },
          grid: {
            color: 'rgba(148, 163, 184, 0.2)',
          },
        },
        x: {
          ticks: {
            color: 'rgba(248, 250, 252, 0.65)',
          },
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  });
}

function runSimulation(inputs) {
  const {
    capacity,
    shiftHours,
    plannedDowntime,
    unplannedProbability,
    qualityRate,
    days,
    shiftsPerDay,
    setupTime,
  } = inputs;

  const results = [];
  let totalDowntimeMinutes = 0;
  let totalScrap = 0;
  let totalGood = 0;
  const minutesPerShift = shiftHours * 60;
  const baseRuntime = minutesPerShift - plannedDowntime;
  const qualityFactor = qualityRate / 100;
  const hourlyCapacity = capacity;
  const idealThroughput = hourlyCapacity * shiftHours;

  for (let day = 0; day < days; day += 1) {
    let dayProduction = 0;
    for (let shift = 0; shift < shiftsPerDay; shift += 1) {
      const unplannedDowntime = simulateUnplannedDowntime({
        shiftHours,
        probability: unplannedProbability,
        setupTime,
      });

      const effectiveRuntime = Math.max(baseRuntime - unplannedDowntime.total, 0);
      const producedUnits = (effectiveRuntime / 60) * hourlyCapacity;
      const goodUnits = producedUnits * qualityFactor;
      const scrapUnits = Math.max(producedUnits - goodUnits, 0);

      dayProduction += goodUnits;
      totalGood += goodUnits;
      totalScrap += scrapUnits;
      totalDowntimeMinutes += plannedDowntime + unplannedDowntime.total + unplannedDowntime.setup;
    }

    results.push({
      day: day + 1,
      goodUnits: dayProduction,
    });
  }

  const totalShifts = days * shiftsPerDay;
  const avgDailyOutput = totalGood / days;
  const perShiftOutput = totalGood / totalShifts;
  const totalRuntime = totalShifts * minutesPerShift;
  const utilization = totalRuntime > 0 ? (totalRuntime - totalDowntimeMinutes) / totalRuntime : 0;
  const performance = perShiftOutput / idealThroughput;
  const quality = qualityFactor;
  const oee = calculateOEE({ availability: utilization, performance, quality });

  return {
    series: results,
    totalDowntimeMinutes,
    totalScrap,
    totalGood,
    avgDailyOutput,
    perShiftOutput,
    utilization,
    performance,
    quality,
    oee,
    throughputPerHour: perShiftOutput / shiftHours,
  };
}

function simulateUnplannedDowntime({ shiftHours, probability, setupTime }) {
  const hours = Math.max(Math.floor(shiftHours), 1);
  let total = 0;
  let setup = 0;

  for (let hour = 0; hour < hours; hour += 1) {
    const eventRoll = Math.random() * 100;
    if (eventRoll < probability) {
      const duration = 5 + Math.random() * 20; // minutos
      total += duration;
    }
  }

  if (total > 0) {
    setup = setupTime;
  }

  return { total, setup };
}

function readInputs() {
  const data = new FormData(configForm);
  return {
    capacity: normalizeNumber(data.get('capacity'), 100),
    shiftHours: normalizeNumber(data.get('shiftHours'), 8),
    plannedDowntime: normalizeNumber(data.get('plannedDowntime'), 30),
    unplannedProbability: normalizeNumber(data.get('unplannedProbability'), 15),
    qualityRate: normalizeNumber(data.get('qualityRate'), 95),
    days: normalizeNumber(data.get('days'), 7),
    shiftsPerDay: normalizeNumber(data.get('shiftsPerDay'), 1),
    setupTime: normalizeNumber(data.get('setupTime'), 20),
  };
}

function updateHero({ utilization, avgDailyOutput, totalDowntimeMinutes }) {
  selectors.efficiency.textContent = formatPercentage(utilization);
  selectors.output.textContent = `${formatNumber(avgDailyOutput, {
    maximumFractionDigits: 0,
  })} un`;
  selectors.downtime.textContent = formatHours(totalDowntimeMinutes / Math.max(readInputs().days, 1));
}

function updateChips({ utilization, oee, throughputPerHour }) {
  selectors.chipUtilization.textContent = `Utilização ${formatPercentage(utilization)}`;
  selectors.chipOee.textContent = `OEE ${formatPercentage(oee)}`;
  selectors.chipThroughput.textContent = `Fluxo ${formatNumber(throughputPerHour, {
    maximumFractionDigits: 0,
  })} un/h`;
}

function updateStats({ avgDailyOutput, totalDowntimeMinutes, totalScrap, perShiftOutput }) {
  selectors.avgDailyOutput.textContent = `${formatNumber(avgDailyOutput, {
    maximumFractionDigits: 0,
  })} unidades`;
  selectors.totalDowntime.textContent = formatHours(totalDowntimeMinutes);
  selectors.scrapAmount.textContent = `${formatNumber(totalScrap, {
    maximumFractionDigits: 0,
  })} unidades`;
  selectors.perShiftOutput.textContent = `${formatNumber(perShiftOutput, {
    maximumFractionDigits: 0,
  })} unidades`;
}

function updateChart(series, days) {
  const labels = series.map((item) => `Dia ${item.day}`);
  const data = series.map((item) => Math.round(item.goodUnits));
  selectors.chartTag.textContent = `Últimos ${days} dias`;
  const canvas = document.getElementById('production-chart').getContext('2d');
  buildChart(canvas, labels, data);
}

function simulateAndRender() {
  const inputs = readInputs();
  const results = runSimulation(inputs);
  updateHero({
    utilization: results.utilization,
    avgDailyOutput: results.avgDailyOutput,
    totalDowntimeMinutes: results.totalDowntimeMinutes,
  });
  updateChips(results);
  updateStats(results);
  updateChart(results.series, inputs.days);
}

selectors.simulateButton.addEventListener('click', simulateAndRender);
selectors.resetButton.addEventListener('click', () => {
  setTimeout(simulateAndRender, 0);
});

simulateAndRender();
