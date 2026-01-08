// ========================================
// Toggle Password Visibility
// ========================================
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Cambiar icono
        const icon = this.querySelector('i');
        if (type === 'password') {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        } else {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        }
    });
}

// ========================================
// Validación del Formulario
// ========================================
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const usernameError = document.getElementById('usernameError');
const passwordError = document.getElementById('passwordError');

// Validar en tiempo real
usernameInput.addEventListener('input', function() {
    if (this.value.trim() === '') {
        showError(usernameError, 'El usuario es requerido');
    } else if (this.value.length < 3) {
        showError(usernameError, 'El usuario debe tener al menos 3 caracteres');
    } else {
        hideError(usernameError);
    }
});

passwordInput.addEventListener('input', function() {
    if (this.value.trim() === '') {
        showError(passwordError, 'La contraseña es requerida');
    } else if (this.value.length < 6) {
        showError(passwordError, 'La contraseña debe tener al menos 6 caracteres');
    } else {
        hideError(passwordError);
    }
});

// Validar al enviar con AJAX
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitBtn = this.querySelector('.btn-primary');
        
        // Deshabilitar botón
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando sesión...';
        submitBtn.disabled = true;
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                showAlert(data.message, 'success');
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1500);
            } else {
                showAlert(data.message, 'error');
                if (typeof grecaptcha !== 'undefined') {
                    grecaptcha.reset();
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error de conexión. Intenta de nuevo.', 'error');
            // No redirigir, mantener en login
        })
        .finally(() => {
            // Rehabilitar botón
            submitBtn.innerHTML = '<span>Iniciar Sesión</span><i class="fas fa-arrow-right"></i>';
            submitBtn.disabled = false;
        });
    });
}

// Funciones auxiliares
function showError(element, message) {
    element.textContent = message;
    element.classList.add('active');
    element.previousElementSibling.querySelector('.form-input').style.borderColor = '#dc3545';
}

function hideError(element) {
    element.textContent = '';
    element.classList.remove('active');
    element.previousElementSibling.querySelector('.form-input').style.borderColor = '#e0e0e0';
}

// ========================================
// Auto-cerrar mensajes después de 5 segundos
// ========================================
const alerts = document.querySelectorAll('.alert');
if (alerts.length > 0) {
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

// ========================================
// Animación de entrada de inputs
// ========================================
const formInputs = document.querySelectorAll('.form-input');
formInputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });

    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// ========================================
// Prevenir envío múltiple del formulario
// ========================================
let isSubmitting = false;

if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        if (isSubmitting) {
            e.preventDefault();
            return false;
        }

        // Validar antes de permitir envío
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (username && password && username.length >= 3 && password.length >= 6) {
            isSubmitting = true;
            const submitBtn = this.querySelector('.btn-submit');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Iniciando sesión...';
            submitBtn.style.opacity = '0.7';
            submitBtn.style.pointerEvents = 'none';
        }
    });
}

// ========================================
// Enter en username pasa a password
// ========================================
if (usernameInput) {
    usernameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            passwordInput.focus();
        }
    });
}

// ========================================
// Recordar usuario (localStorage)
// ========================================
const rememberCheckbox = document.getElementById('remember');
const savedUsername = localStorage.getItem('rememberedUsername');

// Cargar usuario guardado
if (savedUsername && usernameInput) {
    usernameInput.value = savedUsername;
    if (rememberCheckbox) {
        rememberCheckbox.checked = true;
    }
}

// Guardar/eliminar usuario al hacer login
if (loginForm && rememberCheckbox) {
    loginForm.addEventListener('submit', function() {
        if (rememberCheckbox.checked) {
            localStorage.setItem('rememberedUsername', usernameInput.value);
        } else {
            localStorage.removeItem('rememberedUsername');
        }
    });
}

// ========================================
// Función para mostrar alertas
// ========================================
function showAlert(message, type) {
    // Remover alertas existentes
    const existingAlerts = document.querySelectorAll('.dynamic-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Crear nueva alerta
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} dynamic-alert`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Insertar en el DOM
    const container = document.querySelector('.form-container');
    container.insertBefore(alert, container.firstChild);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}

// ========================================
// Console branding
// ========================================
console.log('%c🎓 IntelliTutor UNAM', 'color: #003366; font-size: 24px; font-weight: bold;');
console.log('%cFES Cuautitlán Campo 4', 'color: #FFB800; font-size: 14px;');