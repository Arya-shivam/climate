        document.addEventListener('DOMContentLoaded', (event) => {
            // Assuming other_products is a JavaScript array defined elsewhere in the script
            other_products.forEach((product, index) => {
                var ctx = document.getElementById(`chart-${index + 1}`).getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        datasets: [{
                            label: product.name,
                            data: product.graph_data,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            });
        });