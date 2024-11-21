document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${email}&password=${password}`
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/';
        } else {
            document.getElementById('error-message').style.display = 'block';
        }
    });
});

document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `email=${email}&password=${password}`
    }).then(response => {
        if (response.ok) {
            alert('Registrierung erfolgreich! Bitte loggen Sie sich ein.');
            window.location.href = '/login';
        } else {
            alert('Registrierung fehlgeschlagen!');
        }
    });
});

document.getElementById('file-input').addEventListener('change', function(event) {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = '';
    Array.from(event.target.files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `<span>${file.name}</span>`;
        fileList.appendChild(fileItem);
    });
});