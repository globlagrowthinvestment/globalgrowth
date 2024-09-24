document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    let chartInstance = null;

    const colorPalette = {
        investments: { background: 'rgba(75, 192, 192, 0.2)', border: 'rgba(75, 192, 192, 1)' },
        revenue: { background: 'rgba(153, 102, 255, 0.2)', border: 'rgba(153, 102, 255, 1)' },
        profit: { background: 'rgba(255, 159, 64, 0.2)', border: 'rgba(255, 159, 64, 1)' }
    };

    function formatCurrency(value) {
        return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(value);
    }

    function generateRandomData(numPoints, min, max) {
        return Array.from({length: numPoints}, () => Math.floor(Math.random() * (max - min + 1)) + min);
    }

    function createGradient(ctx, colorStart, colorEnd) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, colorStart);
        gradient.addColorStop(1, colorEnd);
        return gradient;
    }

    function updateChart(period) {
        if (chartInstance) {
            chartInstance.destroy();
        }

        let numPoints, labelFormat;
        const currentDate = new Date();
        
        switch(period) {
            case 'weekly':
                numPoints = 7;
                labelFormat = {weekday: 'short'};
                currentDate.setDate(currentDate.getDate() - 6);
                break;
            case 'monthly':
                numPoints = 30;
                labelFormat = {month: 'short', day: 'numeric'};
                currentDate.setDate(currentDate.getDate() - 29);
                break;
            case 'yearly':
            default:
                numPoints = 12;
                labelFormat = {month: 'short'};
                currentDate.setMonth(currentDate.getMonth() - 11);
                break;
        }
        
        const labels = Array.from({length: numPoints}, (_, i) => {
            const date = new Date(currentDate);
            date.setDate(currentDate.getDate() + i);
            return date.toLocaleDateString('en-US', labelFormat);
        });

        const data = {
            labels: labels,
            datasets: [
                {
                    label: 'Investments',
                    data: generateRandomData(numPoints, 10000, 50000),
                    borderColor: colorPalette.investments.border,
                    backgroundColor: createGradient(ctx, colorPalette.investments.background, 'rgba(255, 255, 255, 0)'),
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Revenue',
                    data: generateRandomData(numPoints, 20000, 80000),
                    borderColor: colorPalette.revenue.border,
                    backgroundColor: createGradient(ctx, colorPalette.revenue.background, 'rgba(255, 255, 255, 0)'),
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Profit',
                    data: generateRandomData(numPoints, 5000, 30000),
                    borderColor: colorPalette.profit.border,
                    backgroundColor: createGradient(ctx, colorPalette.profit.background, 'rgba(255, 255, 255, 0)'),
                    fill: true,
                    tension: 0.4
                }
            ]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatCurrency(value);
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += formatCurrency(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        };

        chartInstance = new Chart(ctx, config);
        updateLegend(data.datasets);
    }

    function updateLegend(datasets) {
        const legendContainer = document.getElementById('chartLegend');
        legendContainer.innerHTML = '';
        datasets.forEach(dataset => {
            const legendItem = document.createElement('div');
            legendItem.classList.add('flex', 'items-center', 'mr-4', 'mb-2');
            legendItem.innerHTML = `
                <div class="w-4 h-4 mr-2 rounded-full" style="background-color: ${dataset.borderColor}"></div>
                <span class="text-sm font-medium">${dataset.label}</span>
            `;
            legendContainer.appendChild(legendItem);
        });
    }

    document.querySelectorAll('.chart-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.chart-btn').forEach(btn => {
                btn.classList.remove('bg-blue-500', 'text-white');
                btn.classList.add('bg-gray-300', 'text-gray-800');
            });
            this.classList.remove('bg-gray-300', 'text-gray-800');
            this.classList.add('bg-blue-500', 'text-white');
            updateChart(this.id.replace('Btn', ''));
        });
    });

    document.getElementById('datasetToggle').addEventListener('change', function() {
        const selectedValue = this.value;
        chartInstance.data.datasets.forEach(dataset => {
            dataset.hidden = selectedValue !== 'all' && dataset.label.toLowerCase() !== selectedValue;
        });
        chartInstance.update();
    });

    // Initial chart update
    updateChart('yearly');
});