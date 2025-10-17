document.addEventListener('DOMContentLoaded', function() {
    // Variáveis globais
    let agendamentos = [];
    let agendamentoEditando = null;

    // Elementos do DOM
    const agendamentoModal = new bootstrap.Modal(document.getElementById('agendamentoModal'));
    const visualizarModal = new bootstrap.Modal(document.getElementById('visualizarModal'));
    const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    const tbody = document.getElementById('agendamentosTableBody');
    const form = document.getElementById('agendamentoForm');
    const modalTitle = document.getElementById('modalTitle');

    // --- INICIALIZAÇÃO ---
    carregarDadosIniciais();
    configurarEventListeners();

    // --- FUNÇÕES PRINCIPAIS ---

    async function carregarDadosIniciais() {
        mostrarLoading(true);
        try {
            const response = await fetch('/api/agendamentos');
            if (!response.ok) {
                throw new Error(`Erro na rede: ${response.statusText}`);
            }
            agendamentos = await response.json();
            renderizarTabela(agendamentos);
        } catch (error) {
            console.error('Erro ao carregar agendamentos:', error);
            mostrarToast('Falha ao carregar dados. Tente atualizar a página.', 'error');
        } finally {
            mostrarLoading(false);
        }
    }

    function renderizarTabela(dados) {
        tbody.innerHTML = '';
        if (dados.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">Nenhum agendamento encontrado.</td></tr>';
            return;
        }

        dados.forEach(ag => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div>
                        <strong>${formatarData(ag.data)}</strong><br>
                        <small class="text-muted">${ag.hora.substring(0, 5)}</small>
                    </div>
                </td>
                <td>
                    <div>
                        <strong>${ag.cliente_nome}</strong><br>
                        <small class="text-muted">${ag.cliente_telefone}</small>
                    </div>
                </td>
                <td>
                    <div>
                        <strong>${ag.pet_nome}</strong><br>
                        <small class="text-muted">${ag.pet_raca}</small>
                    </div>
                </td>
                <td>${ag.servico_nome}</td>
                <td>${ag.veterinario_nome}</td>
                <td>${ag.sala_nome}</td>
                <td><span class="badge status-${ag.status}">${formatarStatus(ag.status)}</span></td>
                <td>
                    <div class="dropdown">
                        <button class="btn btn-outline-primary btn-sm dropdown-toggle" data-bs-toggle="dropdown">Ações</button>
                        <ul class="dropdown-menu">
                            ${criarBotoesAcao(ag)}
                        </ul>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }

    function criarBotoesAcao(ag) {
        let botoes = `<li><a class="dropdown-item" href="#" data-id="${ag.id}" data-action="visualizar"><i class="fas fa-eye me-2"></i>Visualizar</a></li>`;
        if (ag.status !== 'realizado' && ag.status !== 'cancelado') {
            botoes += `<li><a class="dropdown-item" href="#" data-id="${ag.id}" data-action="editar"><i class="fas fa-edit me-2"></i>Editar</a></li>`;
            if (ag.status === 'agendado') {
                botoes += `<li><a class="dropdown-item" href="#" data-id="${ag.id}" data-action="confirmar"><i class="fas fa-check me-2"></i>Confirmar</a></li>`;
            }
            if (ag.status === 'confirmado') {
                botoes += `<li><a class="dropdown-item" href="#" data-id="${ag.id}" data-action="realizar"><i class="fas fa-user-md me-2"></i>Realizar</a></li>`;
            }
            botoes += `<li><hr class="dropdown-divider"></li>`;
            botoes += `<li><a class="dropdown-item text-danger" href="#" data-id="${ag.id}" data-action="cancelar"><i class="fas fa-times me-2"></i>Cancelar</a></li>`;
        } else if (ag.status === 'realizado') {
            botoes += `<li><a class="dropdown-item" href="#" data-id="${ag.id}" data-action="relatorio"><i class="fas fa-file-medical me-2"></i>Relatório</a></li>`;
        }
        return botoes;
    }

    // --- MANIPULAÇÃO DE EVENTOS ---

    function configurarEventListeners() {
        // Ações da tabela
        tbody.addEventListener('click', (e) => {
            if (e.target.matches('[data-action]')) {
                e.preventDefault();
                const id = e.target.dataset.id;
                const action = e.target.dataset.action;
                const agendamento = agendamentos.find(a => a.id == id);

                switch (action) {
                    case 'visualizar': visualizarAgendamento(agendamento); break;
                    case 'editar': editarAgendamento(agendamento); break;
                    case 'confirmar': confirmarAgendamento(id); break;
                    case 'realizar': realizarAgendamento(id); break;
                    case 'cancelar': cancelarAgendamento(id); break;
                    case 'relatorio': gerarRelatorio(id); break;
                }
            }
        });

        // Filtros
        document.getElementById('searchInput').addEventListener('input', filtrarAgendamentos);
        document.getElementById('statusFilter').addEventListener('change', filtrarAgendamentos);
        // Adicionar outros filtros aqui...

        // Modal
        document.getElementById('agendamentoModal').addEventListener('hidden.bs.modal', limparFormulario);
        form.addEventListener('submit', salvarAgendamento);
    }

    // --- AÇÕES ---

    function visualizarAgendamento(ag) {
        if (!ag) return;
        // Preencher modal de visualização
        document.getElementById('viewCliente').textContent = ag.cliente_nome;
        document.getElementById('viewTelefone').textContent = ag.cliente_telefone;
        document.getElementById('viewPet').textContent = ag.pet_nome;
        document.getElementById('viewRaca').textContent = ag.pet_raca;
        document.getElementById('viewData').textContent = formatarData(ag.data);
        document.getElementById('viewHorario').textContent = ag.hora.substring(0, 5);
        document.getElementById('viewStatus').innerHTML = `<span class="badge status-${ag.status}">${formatarStatus(ag.status)}</span>`;
        document.getElementById('viewServico').textContent = ag.servico_nome;
        document.getElementById('viewVeterinario').textContent = ag.veterinario_nome;
        document.getElementById('viewSala').textContent = ag.sala_nome;
        document.getElementById('viewObservacoes').textContent = ag.observacoes || 'Nenhuma observação registrada.';
        visualizarModal.show();
    }

    function editarAgendamento(ag) {
        if (!ag) return;
        agendamentoEditando = ag.id;
        modalTitle.textContent = 'Editar Agendamento';
        // Preencher formulário (requer mais lógica para mapear nomes para IDs)
        form.elements.data.value = ag.data;
        form.elements.horario.value = ag.hora;
        form.elements.status.value = ag.status;
        form.elements.observacoes.value = ag.observacoes;
        agendamentoModal.show();
    }

    async function salvarAgendamento(e) {
        e.preventDefault();
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const dados = new FormData(form);
        const url = agendamentoEditando ? `/api/agendamentos/${agendamentoEditando}` : '/api/agendamentos';
        const method = agendamentoEditando ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                body: dados
            });
            if (!response.ok) throw new Error('Erro ao salvar agendamento.');

            const resultado = await response.json();
            mostrarToast(resultado.message, 'success');
            agendamentoModal.hide();
            carregarDadosIniciais(); // Recarrega os dados
        } catch (error) {
            mostrarToast(error.message, 'error');
        }
    }

    async function atualizarStatus(id, status) {
        try {
            const response = await fetch(`/api/agendamentos/${id}/status`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status })
            });
            if (!response.ok) throw new Error('Erro ao atualizar status.');

            const resultado = await response.json();
            mostrarToast(resultado.message, 'success');
            carregarDadosIniciais();
        } catch (error) {
            mostrarToast(error.message, 'error');
        }
    }

    function confirmarAgendamento(id) {
        if (confirm('Deseja confirmar este agendamento?')) {
            atualizarStatus(id, 'confirmado');
        }
    }

    function realizarAgendamento(id) {
        if (confirm('Marcar este agendamento como realizado?')) {
            atualizarStatus(id, 'realizado');
        }
    }

    function cancelarAgendamento(id) {
        agendamentoEditando = id;
        confirmDeleteModal.show();
    }

    document.getElementById('confirmarCancelamentoBtn').addEventListener('click', () => {
        if (agendamentoEditando) {
            atualizarStatus(agendamentoEditando, 'cancelado');
            confirmDeleteModal.hide();
            agendamentoEditando = null;
        }
    });

    function gerarRelatorio(id) {
        mostrarToast('Funcionalidade de relatório ainda não implementada.', 'info');
    }

    // --- FUNÇÕES UTILITÁRIAS ---

    function filtrarAgendamentos() {
        const busca = document.getElementById('searchInput').value.toLowerCase();
        const status = document.getElementById('statusFilter').value;

        const filtrados = agendamentos.filter(ag => {
            const noStatus = !status || ag.status === status;
            const naBusca = !busca ||
                            ag.cliente_nome.toLowerCase().includes(busca) ||
                            ag.pet_nome.toLowerCase().includes(busca) ||
                            ag.servico_nome.toLowerCase().includes(busca);
            return noStatus && naBusca;
        });
        renderizarTabela(filtrados);
    }

    function limparFormulario() {
        form.reset();
        agendamentoEditando = null;
        modalTitle.textContent = 'Novo Agendamento';
        definirDataAtual();
    }

    function definirDataAtual() {
        const hoje = new Date().toISOString().split('T')[0];
        document.getElementById('data').value = hoje;
    }

    function mostrarLoading(mostrar) {
        // Implementar um spinner/loading visual
        tbody.innerHTML = mostrar ? '<tr><td colspan="8" class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i></td></tr>' : '';
    }

    function formatarData(dataStr) {
        return new Date(dataStr + 'T00:00:00').toLocaleDateString('pt-BR');
    }

    function formatarStatus(status) {
        const map = { agendado: 'Agendado', confirmado: 'Confirmado', realizado: 'Realizado', cancelado: 'Cancelado' };
        return map[status] || status;
    }

    function mostrarToast(mensagem, tipo = 'info') {
        const toastContainer = document.getElementById('toast-container') || criarToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${tipo} border-0`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${mensagem}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>`;
        toastContainer.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
        bsToast.show();
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
    }

    function criarToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }
});