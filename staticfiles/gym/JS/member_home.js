  // Dark Mode Toggle
  function toggleDarkMode() {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        localStorage.setItem('theme', 'light');
        document.body.classList.remove('dark');
    } else {
        localStorage.setItem('theme', 'dark');
        document.body.classList.add('dark');
    }
}

// Check and apply theme on page load
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
}

// Chart.js Progress Chart
var ctx = document.getElementById('progressChart').getContext('2d');
var progressChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4' ],
        datasets: [{
            label: 'Your Progress',
            data: [10, 20, 30, 50],  // Sample data, should be replaced with actual member progress data
            borderColor: '#34d399',
            backgroundColor: 'rgba(52, 211, 153, 0.2)',
            borderWidth: 3,
            fill: true,
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                ticks: {
                    color: '#fff'
                }
            },
            y: {
                ticks: {
                    color: '#fff'
                }
            }
        }
    }
});

