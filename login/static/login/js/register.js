// Validaciones ahora están en el HTML con onkeypress y oninput

// Toggle password
document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        input.type = input.type === 'password' ? 'text' : 'password';
    });
});

// Función para mostrar alertas
function showAlert(message, type) {
    const existingAlerts = document.querySelectorAll('.dynamic-alert');
    existingAlerts.forEach(alert => alert.remove());
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} dynamic-alert`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    const container = document.querySelector('.form-container');
    container.insertBefore(alert, container.querySelector('.register-form'));
    
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';
        setTimeout(() => alert.remove(), 300);
    }, 4000);
}

// Validación completa del formulario
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Limpiar errores previos
    clearAllErrors();
    
    let hasErrors = false;
    
    // Validar nombre
    const firstName = document.querySelector('input[name="first_name"]');
    if (!firstName.value.trim()) {
        showFieldError('first_name_error', 'El nombre es obligatorio');
        hasErrors = true;
    } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(firstName.value)) {
        showFieldError('first_name_error', 'Solo letras, acentos, ñ y espacios');
        hasErrors = true;
    }
    
    // Validar apellido
    const lastName = document.querySelector('input[name="last_name"]');
    if (!lastName.value.trim()) {
        showFieldError('last_name_error', 'Los apellidos son obligatorios');
        hasErrors = true;
    } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(lastName.value)) {
        showFieldError('last_name_error', 'Solo letras, acentos, ñ y espacios');
        hasErrors = true;
    }
    
    // Validar email
    const email = document.querySelector('input[name="email"]');
    if (!email.value.trim()) {
        showFieldError('email_error', 'El correo es obligatorio');
        hasErrors = true;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showFieldError('email_error', 'Formato de correo inválido');
        hasErrors = true;
    }
    
    // Validar usuario
    const username = document.querySelector('input[name="username"]');
    if (!username.value.trim()) {
        showFieldError('username_error', 'El usuario es obligatorio');
        hasErrors = true;
    }
    
    // Validar teléfono
    const telefono = document.querySelector('input[name="telefono"]');
    if (!telefono.value.trim()) {
        showFieldError('telefono_error', 'El teléfono es obligatorio');
        hasErrors = true;
    } else if (!/^[0-9]{10}$/.test(telefono.value)) {
        showFieldError('telefono_error', 'Exactamente 10 dígitos');
        hasErrors = true;
    }
    
    // Validar contraseña
    const password = document.querySelector('input[name="password"]');
    if (!password.value) {
        showFieldError('password_error', 'La contraseña es obligatoria');
        hasErrors = true;
    }
    
    // Validar confirmación de contraseña
    const passwordConfirm = document.querySelector('input[name="password_confirm"]');
    if (!passwordConfirm.value) {
        showFieldError('password_confirm_error', 'Confirma tu contraseña');
        hasErrors = true;
    } else if (password.value !== passwordConfirm.value) {
        showFieldError('password_confirm_error', 'Las contraseñas no coinciden');
        hasErrors = true;
    }
    
    // Validar términos
    const termsCheckbox = document.getElementById('terms');
    if (!termsCheckbox.checked) {
        showAlert('Debes aceptar los términos y condiciones', 'error');
        hasErrors = true;
    }
    
    // Si no hay errores, enviar formulario
    if (!hasErrors) {
        this.submit();
    }
});

function showFieldError(errorId, message) {
    const errorElement = document.getElementById(errorId);
    const input = errorElement.previousElementSibling.querySelector('.form-control');
    
    errorElement.textContent = message;
    errorElement.classList.add('show');
    input.classList.add('error');
    
    // Auto-ocultar después de 4 segundos
    setTimeout(() => {
        errorElement.classList.remove('show');
        input.classList.remove('error');
    }, 4000);
}

function clearAllErrors() {
    document.querySelectorAll('.error-message').forEach(error => {
        error.classList.remove('show');
        error.textContent = '';
    });
    document.querySelectorAll('.form-control').forEach(input => {
        input.classList.remove('error');
    });
}
// Auto-ocultar mensajes del backend después de 4 segundos
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const messages = document.querySelectorAll('.alert:not(.dynamic-alert)');
        messages.forEach(function(message) {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s ease';
            setTimeout(() => message.remove(), 500);
        });
    }, 4000);
});
