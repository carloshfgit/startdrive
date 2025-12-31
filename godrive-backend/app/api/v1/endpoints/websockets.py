from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from jose import jwt, JWTError
from app.core.config import settings
from app.services.socket_service import socket_manager
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.repositories.ride_repository import RideRepository

router = APIRouter()

@router.websocket("/rides/{ride_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    ride_id: int,
    token: Optional[str] = Query(None)
):
    """
    Endpoint WebSocket para monitoramento em tempo real.
    Requer token JWT via query param: ws://host/api/v1/ws/rides/{id}?token=XYZ
    """
    # 1. Validação do Token (Handshake Manual)
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Token inválido")
    except (JWTError, ValueError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # 2. Validação de Negócio (Usuário e Aula)
    # Criamos uma sessão manual pois WebSockets não usam o Depends(get_db) da mesma forma
    db = SessionLocal()
    try:
        user_repo = UserRepository()
        ride_repo = RideRepository()
        
        user = user_repo.get_by_email(db, email=email)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        ride = ride_repo.get_by_id(db, ride_id)
        if not ride:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        # Segurança: Apenas o Aluno ou o Instrutor daquela aula podem entrar na sala
        is_student = (ride.student_id == user.id)
        is_instructor = (ride.instructor_id == user.id)

        if not (is_student or is_instructor):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
            
        # (Opcional) Validar se a aula está ativa (SCHEDULED ou IN_PROGRESS)
        # if ride.status not in ["scheduled", "in_progress"]:
        #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        #     return

    finally:
        db.close() # Fecha a conexão com o banco após a validação inicial

    # 3. Loop de Comunicação
    await socket_manager.connect(ride_id, websocket)
    try:
        while True:
            # Recebe dados de localização: {"lat": -23.5, "long": -46.6}
            data = await websocket.receive_json()
            
            # Injeta o ID de quem enviou (para o front saber se é o aluno ou instrutor)
            data["sender_id"] = user.id
            
            # Repassa para todos na sala (Broadcast)
            await socket_manager.broadcast_location(ride_id, data)
            
    except WebSocketDisconnect:
        socket_manager.disconnect(ride_id, websocket)