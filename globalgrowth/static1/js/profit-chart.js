const TOTAL_POINTS = 50;
const UPDATE_INTERVAL = 100; // milliseconds
let data = Array(TOTAL_POINTS).fill(0).map(() => Math.random() * 100);
let profit = 20000;
let change = 5.2;

const profitElement = document.getElementById('profit');
const profitChangeIconElement = document.getElementById('profitChangeIcon');
const profitChangePercentElement = document.getElementById('profitChangePercent');
const svgElement = document.getElementById('profitChartSvg');
const pathElement = svgElement.querySelector('path');

function updateChart() {
    const width = svgElement.clientWidth;
    const height = svgElement.clientHeight;
    const padding = 10;
    const maxValue = Math.max(...data);
    const xStep = (width - padding * 2) / (TOTAL_POINTS - 1);

    const points = data
        .map((d, i) => [
            i * xStep + padding,
            height - ((d / maxValue) * (height - padding * 2) + padding),
        ])
        .map(point => point.join(','))
        .join(' ');

    pathElement.setAttribute('d', `M ${points}`);
}

function updateData() {
    const newPoint = data[data.length - 1] + (Math.random() - 0.5) * 10;
    data = [...data.slice(1), newPoint];

    profit = Math.max(0, profit + (Math.random() - 0.5) * 1000);
    change = ((profit - 20000) / 20000) * 100;

    profitElement.textContent = `Ksh ${profit.toFixed(2)}`;
    profitChangePercentElement.textContent = `${Math.abs(change).toFixed(2)}%`;

    if (change >= 0) {
        profitChangeIconElement.className = 'fas fa-arrow-up text-green-600 mr-2';
        profitChangePercentElement.className = 'text-green-600';
    } else {
        profitChangeIconElement.className = 'fas fa-arrow-down text-red-600 mr-2';
        profitChangePercentElement.className = 'text-red-600';
    }

    updateChart();
}

// Initial update
updateChart();

// Start the animation
setInterval(updateData, UPDATE_INTERVAL);

// Handle window resize
window.addEventListener('resize', updateChart);