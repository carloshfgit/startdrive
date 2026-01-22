from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    """
    Gerencia as conexões WebSocket ativas, agrupando-as por 'ride_id'.
    Funciona como uma sala de chat: o que é enviado em uma 'ride_id'
    só é recebido por quem está conectado naquela 'ride_id'.
    """
    def __init__(self):
        # Armazena as conexões ativas: { ride_id: [websocket1, websocket2] }
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, ride_id: int, websocket: WebSocket):
        """
        Aceita a conexão e adiciona o socket à lista daquela aula.
        """
        await websocket.accept()
        ride_key = str(ride_id)
        
        if ride_key not in self.active_connections:
            self.active_connections[ride_key] = []
            
        self.active_connections[ride_key].append(websocket)
        print(f"Nova conexão na aula {ride_id}. Total: {len(self.active_connections[ride_key])}")

    def disconnect(self, ride_id: int, websocket: WebSocket):
        """
        Remove a conexão da lista quando o usuário desconecta.
        """
        ride_key = str(ride_id)
        if ride_key in self.active_connections:
            if websocket in self.active_connections[ride_key]:
                self.active_connections[ride_key].remove(websocket)
                
            # Se a sala ficar vazia, removemos a chave para economizar memória
            if not self.active_connections[ride_key]:
                del self.active_connections[ride_key]
                
        print(f"Desconexão na aula {ride_id}.")

    async def broadcast_location(self, ride_id: int, data: dict):
        """
        Envia os dados de localização para TODOS conectados naquela aula (Aluno e Instrutor).
        """
        ride_key = str(ride_id)
        if ride_key in self.active_connections:
            # Percorre todos os sockets conectados na sala
            for connection in self.active_connections[ride_key]:
                try:
                    # Envia como JSON
                    await connection.send_json(data)
                except Exception as e:
                    print(f"Erro ao enviar dados para socket na aula {ride_id}: {e}")
                    # Em caso de erro (ex: socket fechado abruptamente), poderíamos remover aqui
                    # mas o disconnect normalmente lida com isso.

# Instância global para ser importada nos endpoints
socket_manager = ConnectionManager()