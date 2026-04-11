document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const emailInput = document.getElementById('email');
      const passwordInput = document.getElementById('password');
      const errorMessage = document.getElementById('error-message');

      if (errorMessage) {
        errorMessage.textContent = '';
      }

      const email = emailInput.value.trim();
      const password = passwordInput.value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: email,
            password: password
          })
        });

        const data = await response.json();

        if (response.ok) {
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          if (errorMessage) {
            errorMessage.textContent = data.error || 'Login failed';
          } else {
            alert(data.error || 'Login failed');
          }
        }
      } catch (error) {
        if (errorMessage) {
          errorMessage.textContent = 'Unable to connect to the server';
        } else {
          alert('Unable to connect to the server');
        }
      }
    });
  }
});