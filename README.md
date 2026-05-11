# Arquitectura Oficial

El backend es la fuente de verdad.

Tecnologías:
- Backend: FastAPI
- DB: Supabase PostgreSQL
- Auth: Twitch OAuth
- Frontend: Vue 3 + Vite + GSAP

# Reglas críticas

1. El frontend debe adaptarse al backend.
2. No modificar endpoints existentes sin justificarlo.
3. No usar lógica duplicada en frontend.
4. Toda regla de negocio debe vivir en backend.
5. El frontend solo consume APIs.
6. No usar Supabase directamente desde frontend salvo realtime si se aprueba explícitamente.
7. Mantener compatibilidad con:
   - Sorteos
   - Participantes
   - Chat commands
   - Confirmación por chat
   - Expiración de confirmación
   - Overlay OBS
   - GSAP animations

# Objetivo

Eliminar dependencias antiguas:
- Supabase JS directo
- Edge Functions antiguas
- Reglas de negocio en frontend

y migrar el frontend a consumir exclusivamente el backend FastAPI.
