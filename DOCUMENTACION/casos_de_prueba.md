# Casos de Prueba — Chatbot de Gestión de Rechazos Logísticos

**TPI Organización Empresarial — TUP a Distancia (UTN)**
**Autores:** Rodolfo Gutiérrez, Lucía Gutiérrez

Este documento reúne los casos de prueba ejecutados sobre `chatbot_rechazos.py`,
cubriendo el "camino feliz" (flujo normal) y el "camino infeliz" (errores de
entrada y casos límite), tal como exige la consigna del TPI.

Todos los casos fueron ejecutados realmente sobre el script (no son hipotéticos).

---

## Camino feliz

### Caso 1 — Ticket simple (1 SKU, 1 lote)
**Objetivo:** validar el flujo completo de punta a punta con el caso más simple.

| Paso | Acción | Resultado esperado |
|---|---|---|
| 1 | Registrar ticket con 1 ítem (SKU 77268155, lote L001, estado informado "Sana") | Se genera TK-0001, estado "Ticket generado" |
| 2 | Actualizar estado → "Pendiente recepción física" → "Mercadería recepcionada" | El ticket avanza de estado |
| 3 | Actualizar estado → "Control físico realizado" | Se solicita motivo final, estado físico final y clasificación por ítem |
| 4 | Actualizar estado → "SAP actualizado" e ingresar EDI | Se registra EDI; como la clasificación es "Apta" → estado SAP = **TC01** |
| 5 | Actualizar estado → "WMS actualizado" | Estado WMS = **AMU** |
| 6 | Cerrar ticket | Se cierra correctamente ("SAP y WMS se encuentran alineados") |

**Resultado obtenido:** ✅ OK. Coincide exactamente con lo esperado.

---

### Caso 2 — Ticket con 2 SKUs distintos
**Objetivo:** validar que un mismo ticket admite múltiples productos diferentes.

- Se registró TK-0002 con 2 ítems: SKU 77274793 (lote L100, "Producto dañado", "Rota") y SKU 77235550 (lote L200, "Sobrestock", "Sana").

**Resultado obtenido:** ✅ OK. Ambos ítems quedan guardados de forma independiente dentro del mismo ticket, cada uno con sus propios datos (SKU, lote, motivo, estado físico).

---

### Caso 3 — Mismo SKU, 2 lotes distintos
**Objetivo:** validar que el sistema distingue ítems por lote aunque el SKU sea el mismo (caso real: una devolución puede incluir el mismo producto de dos lotes/vencimientos distintos).

- Se registró TK-0003 con 2 ítems, ambos SKU 77268155, pero lotes LA01 y LA02, con cantidades y vencimientos distintos.

**Resultado obtenido:** ✅ OK. El sistema no agrupa por SKU: cada ítem se guarda y se muestra por separado, identificado por lote. Esto es importante para la trazabilidad real del depósito.

---

### Caso 4 — Divergencia entre motivo/estado informado por el cliente y lo determinado por CDM
**Objetivo:** validar que el sistema permite que el control físico determine algo distinto a lo informado inicialmente (esto es central en el proceso real, según el informe).

- Se registró un ticket con estado físico informado "Sana".
- En el control físico (CDM), se cambió a motivo final "Producto dañado", estado físico final "Rota", clasificación "No apta".

**Resultado obtenido:** ⚠️ OK con observación. El sistema sí permite la divergencia y la clasificación final correcta queda registrada. **Pero el campo "estado físico" se sobrescribe**: una vez hecho el control físico, se pierde el dato de que el cliente había informado "Sana". Solo se conserva el valor final ("Rota").
A diferencia del **motivo**, que sí guarda por separado `motivo_inicial` y `motivo_final`, el **estado físico** no tiene esa distinción en el modelo de datos. Es una inconsistencia menor entre cómo se diseñó el campo "motivo" y cómo se diseñó el campo "estado físico" — vale la pena mencionarlo en el informe o corregirlo (agregar `estado_fisico_inicial` / `estado_fisico_final`).

---

### Caso 5 — Mercadería no apta para la venta
**Objetivo:** validar la actualización SAP/WMS cuando la clasificación final es "No apta".

- Mismo ticket del Caso 4 (clasificación final "No apta").

**Resultado obtenido:** ✅ OK.
- SAP → **TC02 - Stock no apto para la venta**
- WMS → **SCP - Mercadería no apta para la venta**

Coincide con lo descripto en el informe (sección 10).

---

### Caso 6 — Ticket con varios ítems, resultado mixto (algunos aptos, otros no)
**Objetivo:** validar qué pasa cuando dentro de un mismo ticket hay ítems con clasificación final distinta entre sí.

- Se registró un ticket con 3 ítems. En el control físico: Ítem 1 → Apta, Ítem 2 → No apta, Ítem 3 → Apta.

**Resultado obtenido:** ✅ OK, con un punto a discutir en el coloquio. El detalle por ítem se conserva correctamente (cada uno muestra su propia clasificación). Pero el estado **SAP y WMS se calcula a nivel de TICKET completo, no por ítem**: alcanza con que **un solo ítem** sea "No apta" para que TODO el ticket (incluidos los ítems aptos) quede registrado como **TC02 / SCP**.
Esto puede ser intencional (todo el delivery se trata como una sola unidad administrativa) o puede ser una simplificación a mejorar. Es una excelente pregunta para anticipar en el coloquio: *"¿por qué la clasificación es a nivel ticket y no a nivel ítem?"*

---

## Camino infeliz (errores de entrada y casos límite)

### Caso 7 — Opción de menú inválida
**Entrada:** se ingresó "9" en el menú principal (solo existen opciones 1-6).
**Resultado obtenido:** ✅ OK. Muestra "Opción inválida. Ingrese un número del 1 al 6." y vuelve a mostrar el menú. No se cae el programa.

### Caso 8 — Texto en lugar de número
**Entrada:** al preguntar "¿Cuántos ítems tiene el rechazo?", se ingresó "abc".
**Resultado obtenido:** ✅ OK. Muestra "Error: debe ingresar un número válido." y vuelve a pedir el dato, sin perder lo ya cargado (delivery y cliente).

### Caso 9 — SKU inexistente
**Entrada:** se ingresó el SKU "00000000", que no existe en la base simulada.
**Resultado obtenido:** ✅ OK. Muestra "SKU inexistente en la base simulada." y lista los SKUs válidos disponibles, sin perder el resto de la carga.

### Caso 10 — Consultar un ticket que no existe
**Entrada:** se consultó "TK-9999".
**Resultado obtenido:** ✅ OK. Muestra "No se encontró el ticket solicitado." sin romper el programa.

### Caso 11 — Cerrar un ticket sin completar SAP/EDI
**Entrada:** se intentó cerrar un ticket recién creado, sin haber registrado EDI ni actualizado SAP/WMS.
**Resultado obtenido:** ✅ OK. Muestra "No se puede cerrar el ticket: falta registrar EDI." y no permite el cierre. (Las validaciones de SAP y WMS pendientes están en el código pero no llegamos a probarlas porque la de EDI corta primero — están escritas con la misma lógica, así que es consistente.)

### Caso 12 — ⚠️ Saltear pasos del proceso (hallazgo no contemplado en la lista original)
**Objetivo:** ver qué pasa si se actualiza el estado del ticket directamente a "SAP actualizado" sin pasar por "Pendiente recepción física", "Mercadería recepcionada" ni "Control físico realizado".
**Resultado obtenido:** 🔴 **Hallazgo importante.** El sistema lo permite sin ninguna advertencia. El ticket queda con EDI generado y SAP en estado **TC01 (apto para la venta)** — el valor "apto" por defecto — **a pesar de que la mercadería nunca fue controlada físicamente** (la clasificación del ítem queda en "Pendiente").
Esto contradice el modelo BPMN descripto en el informe, donde el control físico es un paso obligatorio antes de la actualización en SAP. Es el hallazgo más importante de todo el testing: conviene decidir entre dos caminos:
1. Agregar una validación en `actualizar_estado()` que impida pasar a "SAP actualizado" si el ticket no pasó antes por "Control físico realizado", o
2. Si no da el tiempo para programarlo, dejarlo documentado como **limitación conocida** en el informe (sección de robustez/camino infeliz) — esto también suma puntos, porque demuestra que el equipo identificó el problema aunque no lo haya resuelto en código.

---

## Resumen ejecutivo de testing

| # | Caso | Resultado |
|---|---|---|
| 1 | Ticket simple, 1 SKU | ✅ OK |
| 2 | 2 SKUs distintos | ✅ OK |
| 3 | Mismo SKU, 2 lotes | ✅ OK |
| 4 | Divergencia cliente vs CDM | ⚠️ OK con observación (estado físico se sobrescribe) |
| 5 | Mercadería no apta | ✅ OK |
| 6 | Varios ítems, resultado mixto | ✅ OK (clasificación a nivel ticket, no ítem) |
| 7 | Opción de menú inválida | ✅ OK |
| 8 | Texto en lugar de número | ✅ OK |
| 9 | SKU inexistente | ✅ OK |
| 10 | Ticket inexistente | ✅ OK |
| 11 | Cierre sin EDI | ✅ OK |
| 12 | Saltear pasos del proceso | 🔴 Limitación a documentar/corregir |

**Conclusión del testing:** el chatbot no se cae ante ningún caso probado (0 errores no controlados / 0 crashes). El único hallazgo relevante es de **lógica de negocio** (no de programación): el sistema no obliga a respetar el orden de los estados del proceso.
