# Manual de Usuario — Chatbot de Gestión de Rechazos Logísticos

Guía rápida para usar el chatbot. No requiere conocimientos técnicos: el sistema
guía al usuario con preguntas paso a paso.

## 1. Abrir el programa

```bash
python3 chatbot_rechazos.py
```

Aparece el menú principal:

```
1. Registrar nuevo ticket
2. Consultar ticket
3. Actualizar estado del ticket
4. Mostrar todos los tickets
5. Cerrar ticket
6. Salir
```

Se elige una opción escribiendo el número y presionando ENTER.

## 2. Registrar un nuevo ticket (opción 1)

El bot va a pedir, en este orden:

1. Número de delivery.
2. Cliente.
3. Cuántos ítems (productos) tiene el rechazo.
4. Por cada ítem: SKU, lote, fecha de vencimiento, cantidad rechazada, motivo
   informado (se elige de una lista) y estado físico informado (Sana / Rota).

Al terminar, el bot entrega un número de ticket (ejemplo: `TK-0001`) que hay que
guardar para consultarlo más adelante.

> 💡 Si el SKU ingresado no existe, el bot avisa y muestra los SKUs disponibles
> para volver a intentar.

## 3. Consultar un ticket (opción 2)

Se ingresa el número de ticket (ejemplo `TK-0001`) y el bot muestra todo el detalle:
estado actual, EDI, estado en SAP, estado en WMS y el detalle de cada ítem.

## 4. Actualizar el estado del ticket (opción 3)

El proceso de un ticket avanza por estos pasos, en este orden:

```
Ticket generado
   ↓
Pendiente recepción física
   ↓
Mercadería recepcionada
   ↓
Control físico realizado  →  acá el bot pide el motivo y la clasificación
                              FINAL determinada por el Centro de Distribución
                              (puede ser distinta a lo informado originalmente)
   ↓
Clasificación final
   ↓
SAP actualizado  →  acá el bot pide el número de EDI generado por SAP
   ↓
WMS actualizado
```

Se ingresa el número de ticket y luego se elige el nuevo estado de la lista que
muestra el bot.

> ⚠️ El bot actualmente **no obliga** a respetar este orden — es responsabilidad
> de quien lo usa avanzar los estados en secuencia para que la información quede
> bien registrada.

## 5. Ver todos los tickets (opción 4)

Muestra un listado resumido de todos los tickets registrados en la sesión (número,
delivery, cliente, estado y cantidad de ítems).

## 6. Cerrar un ticket (opción 5)

Se ingresa el número de ticket. El bot solo permite cerrarlo si ya tiene:

- EDI registrado,
- SAP actualizado,
- WMS actualizado.

Si falta alguno de estos tres pasos, el bot avisa cuál falta y no cierra el ticket.

## 7. Salir (opción 6)

Cierra el programa. **Importante:** los tickets se guardan solo mientras el
programa está abierto (es una simulación en memoria); al cerrar el programa, esa
información no queda guardada en ningún archivo.

## Resumen visual del flujo de uso

```
Abrir programa
   ↓
Registrar Ticket
   ↓
Consultar (para verificar)
   ↓
Actualizar (las veces que sea necesario, hasta llegar a "WMS actualizado")
   ↓
Cerrar Ticket
```
