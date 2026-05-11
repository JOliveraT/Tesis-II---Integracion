# Backend - Sorteos Twitch con IA

Backend desarrollado con **Python + FastAPI** y **Supabase/PostgreSQL** para gestionar sorteos en Twitch con criterios de participación significativa, cálculo de puntaje, selección ponderada de ganador y flujo de confirmación.

Este backend forma parte del proyecto de tesis sobre **participación significativa en sorteos de Twitch**, donde el sistema busca evaluar la calidad de la participación de los viewers considerando mensajes, forma de ingreso, comportamiento y elegibilidad.

---

## 1. Estado actual del proyecto

Hasta este punto se implementó:

- Creación de sorteos.
- Registro de participantes.
- Registro de mensajes simulados del chat.
- Registro de forma de ingreso al sorteo:
  - comando de chat;
  - ingreso manual;
  - canje simulado de puntos del canal.
- Cálculo de puntaje de participación.
- Guardado del score en Supabase.
- Selección ponderada del ganador.
- Manejo de confirmación del ganador:
  - modo instantáneo;
  - modo con confirmación por chat.
- Expiración de candidato ganador si no confirma.
- Auditoría básica del proceso.
- Endpoint de resumen general del sorteo para el frontend.
- Simulación de canje de recompensa de puntos del canal.

---

## 2. Tecnologías usadas

- Python 3.12
- FastAPI
- Uvicorn
- Supabase/PostgreSQL
- Pydantic
- python-dotenv

---

## 3. Estructura actual del backend

```text
Backend/
├─ .venv/
├─ app/
│  ├─ routers/
│  │  ├─ messages.py
│  │  ├─ participants.py
│  │  ├─ raffles.py
│  │  ├─ redemptions.py
│  │  ├─ scoring.py
│  │  └─ winner.py
│  │
│  ├─ schemas/
│  │  ├─ message_schema.py
│  │  ├─ participant_schema.py
│  │  ├─ raffle_schema.py
│  │  ├─ redemption_schema.py
│  │  └─ winner_schema.py
│  │
│  ├─ services/
│  │  ├─ participant_service.py
│  │  ├─ raffle_service.py
│  │  ├─ redemption_service.py
│  │  ├─ scoring_service.py
│  │  └─ winner_service.py
│  │
│  ├─ config.py
│  ├─ database.py
│  └─ main.py
│
├─ .env
├─ .gitignore
├─ README.md
└─ requirements.txt
```

---

## 4. Configuración del entorno

### 4.1 Crear entorno virtual

Desde la carpeta `Backend`:

```powershell
py -3.12 -m venv .venv
```

### 4.2 Activar entorno virtual

```powershell
.venv\Scripts\activate
```

Debe aparecer algo similar a:

```text
(.venv) PS C:\Users\User\Desktop\Tesis II\Backend>
```

### 4.3 Instalar dependencias

Con el entorno virtual activado, ejecutar:

```powershell
pip install -r requirements.txt
```
### 4.4 Guardar dependencias

```powershell
pip freeze > requirements.txt
```

---

## 5. Variables de entorno

Crear un archivo `.env` dentro de la carpeta `Backend`:

```env
SUPABASE_URL=https://TU-PROYECTO.supabase.co
SUPABASE_SERVICE_ROLE_KEY=TU_SERVICE_ROLE_KEY
```

Importante:

- `SUPABASE_URL` debe ser el **Project URL** de Supabase.
- No debe terminar en `/rest/v1`.
- La `SERVICE_ROLE_KEY` solo debe usarse en el backend, nunca en el frontend.

---

## 6. Ejecutar el backend

Desde la carpeta `Backend` y con el entorno virtual activo:

```powershell
uvicorn app.main:app --reload
```

Luego abrir:

```text
http://127.0.0.1:8000/docs
```

También se puede probar:

```text
http://127.0.0.1:8000/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "message": "Backend funcionando correctamente"
}
```

---

## 7. Tablas principales en Supabase

El backend trabaja con las siguientes tablas:

```text
users
twitch_channels
raffles
participants
raffle_participants
participation_entries
chat_messages
channel_point_redemptions
participation_scores
ai_evaluations
raffle_results
audit_logs
social_share_logs
```

Las tablas más usadas en esta etapa son:

- `raffles`
- `participants`
- `raffle_participants`
- `chat_messages`
- `participation_entries`
- `channel_point_redemptions`
- `participation_scores`
- `raffle_results`
- `audit_logs`

---

## 8. Endpoints implementados

### Sorteos

```text
GET  /raffles/
POST /raffles/
GET  /raffles/{raffle_id}/summary
```

### Participantes

```text
GET  /participants/
POST /participants/
```

### Mensajes

```text
GET  /messages/
POST /messages/
```

### Scoring

```text
POST /scoring/calculate/{raffle_id}
```

### Ganador

```text
POST /winner/select/{raffle_id}
POST /winner/start-claim/{raffle_id}
POST /winner/confirm/{raffle_id}
POST /winner/expire/{raffle_id}
```

### Canje de puntos simulado

```text
POST /redemptions/simulate
```

---

## 9. Flujo general del sistema

```text
1. Crear sorteo.
2. Registrar participantes.
3. Registrar mensajes del chat.
4. Registrar forma de ingreso al sorteo.
5. Calcular score de participación.
6. Seleccionar ganador ponderado.
7. Si el modo es instantáneo, el sorteo finaliza.
8. Si el modo requiere confirmación, el candidato debe confirmar presencia.
9. Si confirma, el sorteo finaliza.
10. Si no confirma, el intento expira y el sorteo vuelve a estar activo.
```

---

# 10. Pruebas con JSON

## 10.1 Crear sorteo instantáneo

Endpoint:

```text
POST /raffles/
```

JSON:

```json
{
  "title": "Sorteo instantáneo de prueba",
  "prize_title": "Gift Card Steam S/50",
  "prize_description": "Código digital enviado al ganador",
  "command": "!sorteo",
  "confirmation_mode": "instant",
  "claim_timeout_seconds": 0
}
```

Luego ejecutar:

```text
GET /raffles/
```

Copiar el `id` generado y usarlo como `raffle_id` en los siguientes ejemplos.

---

## 10.2 Crear sorteo con confirmación

Endpoint:

```text
POST /raffles/
```

JSON:

```json
{
  "title": "Sorteo con confirmación de presencia",
  "prize_title": "Gift Card Steam S/100",
  "prize_description": "El ganador debe escribir en el chat para confirmar",
  "command": "!sorteo",
  "confirmation_mode": "chat_confirmation",
  "claim_timeout_seconds": 60
}
```

---

## 10.3 Registrar participante por comando

Endpoint:

```text
POST /participants/
```

JSON:

```json
{
  "raffle_id": "PEGA_AQUI_EL_ID_DEL_SORTEO",
  "username": "viewer_comando",
  "display_name": "Viewer Comando",
  "entry_source": "chat_command",
  "entry_content": "!sorteo"
}
```

---

## 10.4 Registrar participante manualmente

Endpoint:

```text
POST /participants/
```

JSON:

```json
{
  "raffle_id": "PEGA_AQUI_EL_ID_DEL_SORTEO",
  "username": "viewer_manual",
  "display_name": "Viewer Manual",
  "entry_source": "manual",
  "entry_content": "Agregado manualmente desde el panel del streamer"
}
```

---

## 10.5 Registrar mensaje del participante

Endpoint:

```text
POST /messages/
```

JSON:

```json
{
  "raffle_id": "PEGA_AQUI_EL_ID_DEL_SORTEO",
  "participant_username": "viewer_comando",
  "content": "!sorteo"
}
```

Otro mensaje:

```json
{
  "raffle_id": "PEGA_AQUI_EL_ID_DEL_SORTEO",
  "participant_username": "viewer_comando",
  "content": "buen stream"
}
```

Otro mensaje:

```json
{
  "raffle_id": "PEGA_AQUI_EL_ID_DEL_SORTEO",
  "participant_username": "viewer_comando",
  "content": "me gusta esta dinámica"
}
```

---

## 10.6 Simular canje de puntos del canal

Endpoint:

```text
POST /redemptions/simulate
```

JSON:

```json
{
  "raffle_id": "PEGA_AQUI_EL_ID_DEL_SORTEO",
  "username": "viewer_puntos",
  "display_name": "Viewer Puntos",
  "twitch_user_id": "123456789",
  "twitch_redemption_id": "redemption-test-001",
  "reward_id": "reward-sorteo-001",
  "reward_title": "Entrada al sorteo por puntos"
}
```

Este endpoint registra automáticamente:

- participante;
- relación con el sorteo;
- entrada de participación;
- canje de puntos simulado;
- auditoría.

---

## 10.7 Calcular score de participación

Endpoint:

```text
POST /scoring/calculate/{raffle_id}
```

Ejemplo:

```text
POST /scoring/calculate/PEGA_AQUI_EL_ID_DEL_SORTEO
```

Respuesta esperada:

```json
{
  "raffle_id": "...",
  "participants_evaluated": 2,
  "results": [
    {
      "username": "viewer_comando",
      "total_messages": 3,
      "unique_messages": 3,
      "command_used": true,
      "reward_used": false,
      "final_score": 100,
      "eligible": true,
      "reason": "Participación válida con interacción suficiente."
    }
  ]
}
```

También se guardan registros en:

```text
participation_scores
raffle_participants
```

---

## 10.8 Seleccionar ganador ponderado

Endpoint:

```text
POST /winner/select/{raffle_id}
```

Ejemplo:

```text
POST /winner/select/PEGA_AQUI_EL_ID_DEL_SORTEO
```

Si el sorteo es instantáneo, el ganador queda confirmado y el sorteo cambia a:

```text
raffles.status = finished
raffle_results.claim_status = confirmed
```

Si el sorteo requiere confirmación, queda como:

```text
raffles.status = pending_claim
raffle_results.claim_status = waiting_start
```

---

## 10.9 Iniciar tiempo de confirmación

Solo aplica para sorteos con:

```text
confirmation_mode = chat_confirmation
```

Endpoint:

```text
POST /winner/start-claim/{raffle_id}
```

JSON:

```json
{
  "claim_timeout_seconds": 60
}
```

Resultado esperado:

```text
raffle_results.claim_status = pending
claim_started_at = fecha actual
claim_expires_at = fecha actual + segundos definidos
```

---

## 10.10 Confirmar ganador

Endpoint:

```text
POST /winner/confirm/{raffle_id}
```

Uso esperado:

Cuando el viewer ganador escribe en el chat dentro del tiempo permitido, se confirma su presencia.

Resultado esperado:

```text
raffles.status = finished
raffle_results.claim_status = confirmed
confirmed_at = fecha actual
```

---

## 10.11 Expirar confirmación

Endpoint:

```text
POST /winner/expire/{raffle_id}
```

Uso esperado:

Si el candidato ganador no confirma dentro del tiempo definido.

Resultado esperado:

```text
raffles.status = active
raffle_results.claim_status = expired
```

Luego se puede volver a ejecutar:

```text
POST /winner/select/{raffle_id}
```

para elegir otro candidato.

---

## 10.12 Ver resumen completo del sorteo

Endpoint:

```text
GET /raffles/{raffle_id}/summary
```

Ejemplo:

```text
GET /raffles/PEGA_AQUI_EL_ID_DEL_SORTEO/summary
```

Este endpoint devuelve:

- datos del sorteo;
- participantes;
- mensajes;
- entradas de participación;
- scores;
- candidato o ganador actual;
- historial de resultados;
- auditoría.

Es el endpoint recomendado para conectar luego con el frontend en Vue.

---

# 11. Flujo visual recomendado para pruebas

## Flujo A: sorteo instantáneo

```text
1. Crear sorteo instantáneo.
2. Registrar 2 o 3 participantes.
3. Registrar mensajes variados.
4. Ejecutar scoring.
5. Seleccionar ganador.
6. Revisar raffle_results y audit_logs.
```

## Flujo B: sorteo con confirmación

```text
1. Crear sorteo con confirmation_mode = chat_confirmation.
2. Registrar participantes.
3. Registrar mensajes.
4. Ejecutar scoring.
5. Seleccionar candidato ganador.
6. Iniciar tiempo de confirmación.
7. Confirmar o expirar.
8. Revisar estado final del sorteo.
```

## Flujo C: canje de puntos simulado

```text
1. Crear sorteo activo.
2. Ejecutar /redemptions/simulate.
3. Revisar participation_entries.
4. Revisar channel_point_redemptions.
5. Ejecutar scoring.
```

---

# 12. Integración futura con Twitch

Más adelante, Twitch se conectará como fuente real de eventos.

La librería propuesta para Python es:

```text
pyTwitchAPI / twitchAPI
```

La integración futura debería alimentar estos flujos ya existentes:

```text
Mensaje en chat con comando
→ register_participant_in_raffle
→ chat_messages
→ participation_entries

Canje de puntos del canal
→ channel_point_redemptions
→ participation_entries
→ raffle_participants

Mensaje del ganador durante confirmación
→ confirm_winner
→ raffle_results.confirmed
→ raffles.finished
```

---

# 13. Observaciones importantes

- Supabase se usa solo como base de datos.
- No se está usando Supabase Auth por ahora.
- La autenticación relevante a futuro será Twitch OAuth.
- La `service_role_key` nunca debe exponerse en Vue.
- El frontend debe comunicarse con FastAPI, no directamente con Supabase usando credenciales sensibles.
- Los datos de prueba deben usar UUID reales generados por Supabase.
- Si un sorteo queda en estado `finished`, ya no debería aceptar participantes ni seleccionar nuevo ganador.
- Si un sorteo está en `pending_claim`, espera confirmación del candidato ganador.

---
