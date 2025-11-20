from datetime import datetime, timezone
from uuid import UUID
from typing import List, Optional
from backend.models.notificacao import Notificacao
from backend.models.usuario import Usuario


class NotificacaoServico:
    """
    Serviço para gerenciar notificações do sistema.
    
    Responsabilidades:
        - Criar e enviar notificações para usuários
        - Listar notificações não lidas
        - Gerenciar o ciclo de vida das notificações
        - Interagir com a camada de persistência
    """
    
    def __init__(self, repositorio=None):
        """
        Inicializa o serviço de notificações.
        
        Args:
            repositorio: Repositório para persistência (opcional, para testes pode ser None)
        """
        self.repositorio = repositorio
        # Cache em memória para quando não houver repositório
        self._notificacoes_cache: List[Notificacao] = []
    
    def enviar(self, usuario: Usuario, mensagem: str, tipo: str = "info", titulo: str = "Notificação") -> Notificacao:
        """
        Envia uma notificação para um usuário.
        
        Args:
            usuario: Usuário que receberá a notificação
            mensagem: Conteúdo da mensagem
            tipo: Tipo da notificação (padrão: "info")
            titulo: Título da notificação (padrão: "Notificação")
            
        Returns:
            Notificação criada e enviada
            
        Raises:
            ValueError: Se usuário for None ou inválido
            ValueError: Se mensagem for vazia
            
        Example:
            >>> servico = NotificacaoServico()
            >>> notif = servico.enviar(usuario, "Sua consulta foi agendada", "sucesso", "Agendamento")
        """
        # Validações
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        if not usuario.is_ativo():
            raise ValueError("Não é possível enviar notificação para usuário inativo")
        
        if not mensagem or not mensagem.strip():
            raise ValueError("Mensagem não pode ser vazia")
        
        # Cria a notificação
        notificacao = Notificacao(
            usuarioId=usuario.uuid,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            criadaEm=datetime.now(timezone.utc),
            lida=False
        )
        
        # Persiste a notificação
        if self.repositorio:
            self.repositorio.salvar(notificacao)
        else:
            # Fallback para cache em memória (útil para testes)
            self._notificacoes_cache.append(notificacao)
        
        return notificacao
    
    def listarNaoLidas(self, usuario: Usuario) -> List[Notificacao]:
        """
        Lista todas as notificações não lidas de um usuário.
        
        Args:
            usuario: Usuário para buscar notificações
            
        Returns:
            Lista de notificações não lidas, ordenadas por data (mais recentes primeiro)
            
        Raises:
            ValueError: Se usuário for None ou inválido
            
        Example:
            >>> servico = NotificacaoServico()
            >>> nao_lidas = servico.listarNaoLidas(usuario)
            >>> print(f"Você tem {len(nao_lidas)} notificações não lidas")
        """
        # Validações
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        # Busca notificações
        if self.repositorio:
            notificacoes = self.repositorio.buscar_por_usuario(usuario.uuid, lida=False)
        else:
            # Fallback para cache em memória
            notificacoes = [
                n for n in self._notificacoes_cache 
                if n.usuarioId == usuario.uuid and not n.lida
            ]
        
        # Ordena por data (mais recentes primeiro)
        notificacoes_ordenadas = sorted(
            notificacoes, 
            key=lambda n: n.criadaEm, 
            reverse=True
        )
        
        return notificacoes_ordenadas
    
    def listarTodas(self, usuario: Usuario, limite: int = 50) -> List[Notificacao]:
        """
        Lista todas as notificações de um usuário (lidas e não lidas).
        
        Args:
            usuario: Usuário para buscar notificações
            limite: Número máximo de notificações a retornar (padrão: 50)
            
        Returns:
            Lista de notificações ordenadas por data (mais recentes primeiro)
            
        Raises:
            ValueError: Se usuário for None ou inválido
        """
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        # Busca notificações
        if self.repositorio:
            notificacoes = self.repositorio.buscar_por_usuario(usuario.uuid)
        else:
            # Fallback para cache em memória
            notificacoes = [
                n for n in self._notificacoes_cache 
                if n.usuarioId == usuario.uuid
            ]
        
        # Ordena e limita
        notificacoes_ordenadas = sorted(
            notificacoes, 
            key=lambda n: n.criadaEm, 
            reverse=True
        )
        
        return notificacoes_ordenadas[:limite]
    
    def marcarComoLida(self, notificacao_id: UUID | str) -> bool:
        """
        Marca uma notificação como lida.
        
        Args:
            notificacao_id: ID da notificação
            
        Returns:
            True se marcada com sucesso, False se não encontrada
            
        Example:
            >>> servico.marcarComoLida(notificacao.id)
        """
        if self.repositorio:
            notificacao = self.repositorio.buscar_por_id(str(notificacao_id))
            if notificacao:
                notificacao.marcarComoLida()
                self.repositorio.atualizar(notificacao)
                return True
        else:
            # Fallback para cache em memória
            for notif in self._notificacoes_cache:
                if notif.id == str(notificacao_id):
                    notif.marcarComoLida()
                    return True
        
        return False
    
    def marcarTodasComoLidas(self, usuario: Usuario) -> int:
        """
        Marca todas as notificações de um usuário como lidas.
        
        Args:
            usuario: Usuário cujas notificações serão marcadas
            
        Returns:
            Número de notificações marcadas como lidas
            
        Raises:
            ValueError: Se usuário for None ou inválido
        """
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        nao_lidas = self.listarNaoLidas(usuario)
        
        for notificacao in nao_lidas:
            notificacao.marcarComoLida()
            if self.repositorio:
                self.repositorio.atualizar(notificacao)
        
        return len(nao_lidas)
    
    def excluir(self, notificacao_id: UUID | str) -> bool:
        """
        Exclui uma notificação.
        
        Args:
            notificacao_id: ID da notificação a ser excluída
            
        Returns:
            True se excluída com sucesso, False se não encontrada
        """
        if self.repositorio:
            return self.repositorio.excluir(str(notificacao_id))
        else:
            # Fallback para cache em memória
            for i, notif in enumerate(self._notificacoes_cache):
                if notif.id == str(notificacao_id):
                    self._notificacoes_cache.pop(i)
                    return True
        
        return False
    
    def excluirAntigas(self, usuario: Usuario, dias: int = 30) -> int:
        """
        Exclui notificações antigas (lidas) de um usuário.
        
        Args:
            usuario: Usuário cujas notificações antigas serão excluídas
            dias: Notificações lidas mais antigas que X dias serão excluídas (padrão: 30)
            
        Returns:
            Número de notificações excluídas
            
        Raises:
            ValueError: Se usuário for None ou inválido
        """
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        todas = self.listarTodas(usuario, limite=1000)
        agora = datetime.now(timezone.utc)
        contador = 0
        
        for notificacao in todas:
            # Só exclui notificações lidas
            if notificacao.lida:
                idade_em_dias = (agora - notificacao.criadaEm).days
                if idade_em_dias > dias:
                    if self.excluir(notificacao.id):
                        contador += 1
        
        return contador
    
    def contar_nao_lidas(self, usuario: Usuario) -> int:
        """
        Conta o número de notificações não lidas de um usuário.
        
        Args:
            usuario: Usuário para contar notificações
            
        Returns:
            Número de notificações não lidas
            
        Raises:
            ValueError: Se usuário for None ou inválido
        """
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        return len(self.listarNaoLidas(usuario))
    
    def enviar_em_lote(self, usuarios: List[Usuario], mensagem: str, tipo: str = "info", titulo: str = "Notificação") -> List[Notificacao]:
        """
        Envia a mesma notificação para múltiplos usuários.
        
        Args:
            usuarios: Lista de usuários que receberão a notificação
            mensagem: Conteúdo da mensagem
            tipo: Tipo da notificação (padrão: "info")
            titulo: Título da notificação (padrão: "Notificação")
            
        Returns:
            Lista de notificações criadas
            
        Raises:
            ValueError: Se lista de usuários for vazia
            
        Example:
            >>> usuarios_ativos = [u1, u2, u3]
            >>> servico.enviar_em_lote(usuarios_ativos, "Manutenção programada", "aviso")
        """
        if not usuarios:
            raise ValueError("Lista de usuários não pode ser vazia")
        
        notificacoes = []
        for usuario in usuarios:
            try:
                notif = self.enviar(usuario, mensagem, tipo, titulo)
                notificacoes.append(notif)
            except ValueError:
                # Ignora usuários inválidos ou inativos
                continue
        
        return notificacoes
    
    def buscar_por_tipo(self, usuario: Usuario, tipo: str) -> List[Notificacao]:
        """
        Busca notificações de um usuário por tipo.
        
        Args:
            usuario: Usuário para buscar notificações
            tipo: Tipo de notificação a buscar
            
        Returns:
            Lista de notificações do tipo especificado
            
        Raises:
            ValueError: Se usuário for None ou inválido
        """
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        todas = self.listarTodas(usuario, limite=1000)
        return [n for n in todas if n.is_tipo(tipo)]
    
    def buscar_urgentes(self, usuario: Usuario) -> List[Notificacao]:
        """
        Busca notificações urgentes (erro ou alerta) não lidas de um usuário.
        
        Args:
            usuario: Usuário para buscar notificações
            
        Returns:
            Lista de notificações urgentes não lidas
            
        Raises:
            ValueError: Se usuário for None ou inválido
        """
        if usuario is None:
            raise ValueError("Usuário não pode ser None")
        
        if not isinstance(usuario, Usuario):
            raise ValueError("usuario deve ser uma instância de Usuario")
        
        nao_lidas = self.listarNaoLidas(usuario)
        return [n for n in nao_lidas if n.is_urgente()]