// Funcionalidades del Portal Estudiantil - IntelliTutor UNAM
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar dropdown del perfil
    initProfileDropdown();
    
    // Inicializar carrusel
    initCarousel();
    
    // Inicializar mensajes
    initMessages();
    
    // Inicializar animaciones de secciones
    initSectionAnimations();
});

// Dropdown del perfil del usuario
function initProfileDropdown() {
    const profileToggle = document.getElementById('profileToggle');
    const profileDropdown = document.getElementById('profileDropdown');
    const dropdownOverlay = document.getElementById('dropdownOverlay');
    const profileContainer = document.querySelector('.profile-dropdown');

    if (profileToggle && profileDropdown) {
        // Alternar dropdown al hacer clic
        profileToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            profileContainer.classList.toggle('active');
            if (dropdownOverlay) {
                dropdownOverlay.style.display = profileContainer.classList.contains('active') ? 'block' : 'none';
            }
        });

        // Cerrar dropdown al hacer clic en el overlay
        if (dropdownOverlay) {
            dropdownOverlay.addEventListener('click', function() {
                profileContainer.classList.remove('active');
                dropdownOverlay.style.display = 'none';
            });
        }

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (profileContainer && !profileContainer.contains(e.target)) {
                profileContainer.classList.remove('active');
                if (dropdownOverlay) {
                    dropdownOverlay.style.display = 'none';
                }
            }
        });

        // Prevenir cierre al hacer clic dentro del dropdown
        profileDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        // Confirmación para cerrar sesión
        const logoutLinks = document.querySelectorAll('a[href*="logout"], a.logout');
        logoutLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                if (!this.hasAttribute('data-confirmed')) {
                    e.preventDefault();
                    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
                        this.setAttribute('data-confirmed', 'true');
                        this.click();
                    }
                }
            });
        });
    }
}

// Carrusel de imágenes
function initCarousel() {
    const carousel = document.getElementById('carousel');
    const dots = document.querySelectorAll('.carousel-dot');
    let currentSlide = 0;
    const totalSlides = 3;

    if (!carousel || dots.length === 0) return;

    function goToSlide(index) {
        currentSlide = index;
        if (carousel) {
            carousel.style.transform = `translateX(-${currentSlide * 100}%)`;
        }
        
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        goToSlide(currentSlide);
    }

    // Configurar eventos para los puntos
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });

    // Auto-avance cada 4 segundos
    const carouselInterval = setInterval(nextSlide, 4000);

    // Pausar al hacer hover
    carousel.addEventListener('mouseenter', () => clearInterval(carouselInterval));
    carousel.addEventListener('mouseleave', () => {
        clearInterval(carouselInterval);
        setInterval(nextSlide, 4000);
    });
}

// Sistema de mensajes
function initMessages() {
    const messages = document.querySelectorAll('.messages-container .message');
    
    if (messages.length > 0) {
        // Auto-ocultar mensajes después de 5 segundos
        setTimeout(() => {
            messages.forEach(msg => {
                msg.classList.add('hide');
                // Eliminar del DOM después de la animación
                setTimeout(() => msg.remove(), 600);
            });
        }, 5000);
        
        // Permitir cerrar manualmente
        messages.forEach(msg => {
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cssText = `
                background: transparent;
                border: none;
                color: inherit;
                font-size: 18px;
                cursor: pointer;
                margin-left: 10px;
                opacity: 0.7;
                transition: opacity 0.2s;
            `;
            closeBtn.addEventListener('click', () => {
                msg.classList.add('hide');
                setTimeout(() => msg.remove(), 600);
            });
            msg.appendChild(closeBtn);
        });
    }
}

// Animaciones para las secciones
function initSectionAnimations() {
    const sectionCards = document.querySelectorAll('.section-card');
    
    // Animación de entrada escalonada
    sectionCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Efectos hover mejorados
    sectionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 15px 35px rgba(0, 51, 102, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Función para mostrar notificaciones (opcional)
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `demo-notification demo-notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 1000;
        animation: slideInRight 0.3s ease;
        border-left: 4px solid ${type === 'success' ? '#28a745' : '#17a2b8'};
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Animación para notificaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);