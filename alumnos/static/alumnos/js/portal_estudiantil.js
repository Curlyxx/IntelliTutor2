// Funcionalidades del Portal Estudiantil - Demo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar componentes
    initTabs();
    initFilters();
    initProgressCharts();
    initDemoAnimations();
});

// Sistema de pestañas
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remover clase active de todos los botones y paneles
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            // Agregar clase active al botón clickeado y panel correspondiente
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
            
            // Efecto visual
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });
}

// Sistema de filtros por materia
function initFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const practicaCards = document.querySelectorAll('.practica-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const filterValue = this.getAttribute('data-course');
            
            // Remover clase active de todos los botones
            filterBtns.forEach(b => b.classList.remove('active'));
            // Agregar clase active al botón clickeado
            this.classList.add('active');
            
            // Filtrar tarjetas
            practicaCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-course') === filterValue) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
}

// Inicializar gráficos de progreso
function initProgressCharts() {
    const chartCircles = document.querySelectorAll('.chart-circle');
    
    chartCircles.forEach(chart => {
        const percent = chart.getAttribute('data-percent');
        chart.style.setProperty('--percent', `${percent}%`);
    });
}

// Animaciones demo
function initDemoAnimations() {
    // Animación de entrada para las tarjetas
    const demoCards = document.querySelectorAll('.demo-card');
    
    demoCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Efectos hover mejorados
    const interactiveElements = document.querySelectorAll('.practica-card, .evaluacion-card, .btn');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.15)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Simular notificaciones
function showDemoNotification(message, type = 'info') {
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
    
}