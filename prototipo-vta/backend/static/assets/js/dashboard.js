// Funções de Interação da Página do Dashboard
// Este arquivo contém os scripts para interatividade da página de dashboard,
// incluindo logout, navegação, e atualizações dinâmicas.

/**
 * @description Exibe uma confirmação de logout e, se confirmado, simula o logout.
 */
function logout() {
    if (confirm('Tem certeza que deseja sair do sistema?')) {
        alert('Logout realizado com sucesso!');
        // Em um ambiente de produção, redirecionar para a página de login:
        // window.location.href = '/logout';
    }
}

/**
 * @description Funções para os botões de "Ações Rápidas".
 * Simulam o redirecionamento para outras páginas.
 */
function novoAgendamento() {
    alert('Redirecionando para tela de novo agendamento...');
    // window.location.href = 'agendamento.html';
}

function novoCliente() {
    alert('Redirecionando para cadastro de cliente...');
    // window.location.href = 'cliente.html';
}

function verAgenda() {
    alert('Redirecionando para visualização da agenda...');
    window.location.href = '/agenda';
}

function gerarRelatorio() {
    alert('Redirecionando para geração de relatórios...');
    // window.location.href = 'relatorios.html';
}

// Delegação de Eventos para o Menu de Navegação
document.addEventListener('DOMContentLoaded', () => {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
        navMenu.addEventListener('click', (e) => {
            const link = e.target.closest('.nav-link');
            if (link) {
                e.preventDefault();

                // Remove a classe 'active' de todos os links
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

                // Adiciona a classe 'active' ao link clicado
                link.classList.add('active');

                // Simula a navegação
                const linkText = link.innerText.trim();
                if (linkText !== 'Dashboard') {
                    alert(`Navegando para: ${linkText}`);
                }
            }
        });
    }

    // Animação "Fade-in" para os Cards de Estatística
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 }); // O callback é chamado quando 10% do elemento está visível

        statCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.6s ease';
            observer.observe(card);
        });
    }

    /**
     * @description Simula a atualização em tempo real das estatísticas para dar dinamismo à página.
     */
    function updateStats() {
        const consultasTodayElement = document.querySelector('.stat-value');
        if (consultasTodayElement) {
            let currentValue = parseInt(consultasTodayElement.textContent);

            // Simula uma mudança aleatória
            if (Math.random() > 0.7) {
                const change = Math.floor(Math.random() * 3) - 1; // -1, 0, ou +1
                const newValue = Math.max(0, currentValue + change);
                consultasTodayElement.textContent = newValue;

                // Animação sutil para a mudança
                consultasTodayElement.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    consultasTodayElement.style.transform = 'scale(1)';
                }, 200);
            }
        }
    }

    // Inicia a atualização simulada a cada 30 segundos
    setInterval(updateStats, 30000);
});
