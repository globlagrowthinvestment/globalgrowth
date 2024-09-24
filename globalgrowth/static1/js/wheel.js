// This is a simplified version. You might want to use a library like GreenSock for more advanced animations.

const wheel = document.getElementById('spin-wheel');
const spinButton = document.getElementById('spin-button');
const ticketList = document.getElementById('ticket-list');

function createWheel(segments) {
    // Create wheel segments
    for (let i = 0; i < segments; i++) {
        const segment = document.createElement('div');
        segment.className = 'wheel-segment';
        segment.style.transform = `rotate(${i * (360 / segments)}deg)`;
        segment.textContent = i + 1;
        wheel.appendChild(segment);
    }
}

function spinWheel() {
    fetch('/globalspin/spin-wheel/', {method: 'POST', headers: {'X-CSRFToken': getCookie('csrftoken')}})
        .then(response => response.json())
        .then(data => {
            if (data.winning_number) {
                const rotation = (360 * 5) + (data.winning_number * (360 / wheel.children.length));
                wheel.style.transition = 'transform 5s cubic-bezier(0.25, 0.1, 0.25, 1)';
                wheel.style.transform = `rotate(${rotation}deg)`;
                setTimeout(() => {
                    alert(`You won! Winning number: ${data.winning_number}`);
                    // Update the ticket list
                    updateTicketList();
                }, 5000);
            } else {
                alert('Error: ' + data.error);
            }
        });
}

function updateTicketList() {
    fetch('/globalspin/dashboard/')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newTicketList = doc.getElementById('ticket-list');
            ticketList.innerHTML = newTicketList.innerHTML;
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize the wheel with 10 segments
createWheel(10);

spinButton.addEventListener('click', spinWheel);