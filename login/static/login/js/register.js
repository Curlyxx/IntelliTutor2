// Toggle password
document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = document.getElementById(btn.dataset.target);
        input.type = input.type === 'password' ? 'text' : 'password';
    });
});

// Solo números
const acc = document.getElementById('account_number');
if(acc){
    acc.addEventListener('input', () => {
        acc.value = acc.value.replace(/\D/g, '');
    });
}

    // Validación del checkbox de términos
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        const termsCheckbox = document.getElementById('terms');
        if (!termsCheckbox.checked) {
            e.preventDefault();
            alert('Debes aceptar los términos y condiciones para continuar.');
            termsCheckbox.focus();
        }
    });

    // Opcional: Habilitar/deshabilitar botón basado en el checkbox
    document.getElementById('terms').addEventListener('change', function() {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = !this.checked;
    });

    // Inicializar el botón como deshabilitado
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('submitBtn').disabled = true;
    });
        // Auto-ocultar mensajes después de 5 segundos
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const messages = document.querySelectorAll('.global-messages-container .alert');
                messages.forEach(function(message) {
                    message.style.opacity = '0';
                    message.style.transition = 'opacity 0.5s ease';
                    setTimeout(() => message.remove(), 500);
                });
            }, 5000);
        });
