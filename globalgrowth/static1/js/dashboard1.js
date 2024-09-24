// Function to format currency
const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES' }).format(amount);
};

// Function to update today's sign-ups
let todaySignups = 0;
const updateTodaySignups = () => {
    todaySignups += 2;
    document.getElementById('today-signups').textContent = todaySignups;
};

// Function to update total investments
let totalInvestments = 30000;
const updateTotalInvestments = () => {
    totalInvestments += 2000;
    document.getElementById('total-investments').textContent = formatCurrency(totalInvestments);
};

// Function to update referrals
let referrals = 10;
const updateReferrals = () => {
    referrals += 1;
    document.getElementById('referrals').textContent = referrals;
};

// Function to update profit
let profit = 20000;
const updateProfit = () => {
    const change = Math.floor(Math.random() * 2000) - 1000; // Random change between -1000 and 1000
    profit += change;
    const profitElement = document.getElementById('profit');
    profitElement.textContent = formatCurrency(profit);
    
    const profitChangeElement = profitElement.nextElementSibling.lastElementChild;
    const profitChangeIconElement = profitElement.nextElementSibling.firstElementChild;
    
    if (change >= 0) {
        profitChangeElement.textContent = `+${(change / profit * 100).toFixed(2)}%`;
        profitChangeElement.classList.remove('text-red-600');
        profitChangeElement.classList.add('text-green-600');
        profitChangeIconElement.classList.remove('fa-arrow-down', 'text-red-600');
        profitChangeIconElement.classList.add('fa-arrow-up', 'text-green-600');
    } else {
        profitChangeElement.textContent = `${(change / profit * 100).toFixed(2)}%`;
        profitChangeElement.classList.remove('text-green-600');
        profitChangeElement.classList.add('text-red-600');
        profitChangeIconElement.classList.remove('fa-arrow-up', 'text-green-600');
        profitChangeIconElement.classList.add('fa-arrow-down', 'text-red-600');
    }
};

// Function to update investment growth
let investmentGrowth = 25000;
const updateInvestmentGrowth = () => {
    const change = Math.floor(Math.random() * 1000) - 200; // Random change between -200 and 800
    investmentGrowth += change;
    const growthElement = document.getElementById('investment-growth');
    growthElement.textContent = formatCurrency(investmentGrowth);
    
    const growthChangeElement = growthElement.nextElementSibling.lastElementChild;
    const growthChangeIconElement = growthElement.nextElementSibling.firstElementChild;
    
    if (change >= 0) {
        growthChangeElement.textContent = `+${(change / investmentGrowth * 100).toFixed(2)}%`;
        growthChangeElement.classList.remove('text-red-600');
        growthChangeElement.classList.add('text-blue-600');
        growthChangeIconElement.classList.remove('fa-arrow-down', 'text-red-600');
        growthChangeIconElement.classList.add('fa-arrow-up', 'text-blue-600');
    } else {
        growthChangeElement.textContent = `${(change / investmentGrowth * 100).toFixed(2)}%`;
        growthChangeElement.classList.remove('text-blue-600');
        growthChangeElement.classList.add('text-red-600');
        growthChangeIconElement.classList.remove('fa-arrow-up', 'text-blue-600');
        growthChangeIconElement.classList.add('fa-arrow-down', 'text-red-600');
    }
};

// Function to update performance chart
const updatePerformanceChart = () => {
    const ctx = document.getElementById('performanceChart').getContext('2d');
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const data = labels.map(() => Math.floor(Math.random() * 50000) + 10000);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Investment Performance',
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value, index, values) {
                            return formatCurrency(value);
                        }
                    }
                }
            }
        }
    });
};

// Function to add recent activities
const addRecentActivity = () => {
    const activities = [
        'New investment made',
        'Withdrawal processed',
        'Referral bonus added',
        'Profile updated',
        'New user registered'
    ];
    const randomActivity = activities[Math.floor(Math.random() * activities.length)];
    const activityElement = document.createElement('li');
    activityElement.className = 'flex items-center space-x-2';
    activityElement.innerHTML = `
        <i class="fas fa-circle text-blue-500 text-xs"></i>
        <span>${randomActivity}</span>
        <span class="text-gray-500 text-sm">${new Date().toLocaleTimeString()}</span>
    `;
    const recentActivitiesList = document.getElementById('recent-activities');
    recentActivitiesList.insertBefore(activityElement, recentActivitiesList.firstChild);
    if (recentActivitiesList.children.length > 5) {
        recentActivitiesList.removeChild(recentActivitiesList.lastChild);
    }
};

// Set up intervals for updates
setInterval(updateTodaySignups, 5 * 60 * 1000); // Every 5 minutes
setInterval(updateTotalInvestments, 60 * 60 * 1000); // Every 1 hour
setInterval(updateReferrals, 60 * 60 * 1000); // Every 1 hour
setInterval(updateProfit, 5 * 60 * 1000); // Every 5 minutes
setInterval(updateInvestmentGrowth, 15 * 60 * 1000); // Every 15 minutes
setInterval(addRecentActivity, 2 * 60 * 1000); // Every 2 minutes

// Initial updates
updateTodaySignups();
updateTotalInvestments();
updateReferrals();
updateProfit();
updateInvestmentGrowth();
updatePerformanceChart();
addRecentActivity();

// Mobile sidebar toggle
document.getElementById('sidebar-toggle').addEventListener('click', () => {
    document.getElementById('mobile-sidebar').classList.toggle('-translate-x-full');
});

document.getElementById('close-sidebar').addEventListener('click', () => {
    document.getElementById('mobile-sidebar').classList.add('-translate-x-full');
});