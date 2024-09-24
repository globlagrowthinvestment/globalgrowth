javascript
Copy
function showToast(message) {
  var toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = "toast show";
  setTimeout(function() {
    toast.className = toast.className.replace("show", "");
  }, 3000);
}

document.getElementById('withdrawalForm').addEventListener('submit', function(event) {
  event.preventDefault();

  var username = document.getElementById('username').value;
  if (username.trim() === '') {
    showToast('Please enter your username.');
    return;
  }

  var phone = document.getElementById('phone').value;
  var phoneRegex = /^[0-9]{10}$/;
  if (!phoneRegex.test(phone)) {
    showToast('Please enter a valid 10-digit phone number.');
    return;
  }

  var amount = document.getElementById('amount').value;
  if (amount <= 0) {
    showToast('Please enter a valid withdrawal amount.');
    return;
  }

  showToast('Request submitted successfully! Redirecting to dashboard...');

  setTimeout(function() {
    window.location.href = "{% url 'dashboard:dashboard' %}";
  }, 3000);
});