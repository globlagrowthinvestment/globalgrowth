document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Deposit form submission
    document.getElementById('deposit-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const mpesaMessage = document.getElementById('mpesa-message').value;
        
        fetch('/user_account/deposit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `mpesa_message=${encodeURIComponent(mpesaMessage)}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.status === 'success') {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Investment form submission
    document.getElementById('investment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const amount = document.getElementById('investment-amount').value;
        
        fetch('/user_account/investment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `amount=${encodeURIComponent(amount)}`
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.status === 'success') {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Start investment buttons
    document.querySelectorAll('.start-investment').forEach(button => {
        button.addEventListener('click', function() {
            const investmentId = this.getAttribute('data-id');
            
            fetch(`/user_account/start_investment/${investmentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                if (data.status === 'success') {
                    location.reload();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Check investment status buttons
    document.querySelectorAll('.check-investment').forEach(button => {
        button.addEventListener('click', function() {
            const investmentId = this.getAttribute('data-id');
            
            fetch(`/user_account/check_investment/${investmentId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(data.message);
                    location.reload();
                } else if (data.status === 'ongoing') {
                    alert(`Investment is still ongoing. Time left: ${data.time_left}`);
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Function to update account information
    function updateAccountInfo() {
        fetch('/user_account/get_account_info/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('account-balance').textContent = `Ksh ${data.balance}`;
            document.getElementById('total-deposits').textContent = `Ksh ${data.total_deposits}`;
            document.getElementById('total-investments').textContent = `Ksh ${data.total_investments}`;
        })
        .catch(error => console.error('Error:', error));
    }

    // Update account info every 30 seconds
    setInterval(updateAccountInfo, 30000);
});