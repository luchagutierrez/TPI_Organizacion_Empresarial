"""
CHATBOT - Gestión de Rechazos Logísticos
TPI Organización Empresarial

Simulación por consola en Python.
Permite registrar tickets de rechazo con múltiples ítems, consultar, actualizar estados,
registrar EDI, definir SAP/WMS y cerrar tickets.
"""

from datetime import datetime

PRODUCTOS = {
    "77268155": "Producto Ferrero SKU 77268155",
    "77274793": "Producto Ferrero SKU 77274793",
    "77235550": "Producto Ferrero SKU 77235550",
    "77235534": "Producto Ferrero SKU 77235534",
    "77277457": "Producto Ferrero SKU 77277457",
}

MOTIVOS = [
    "Sobrestock",
    "Producto dañado",
    "Faltante",
    "No pedido",
    "Producto incorrecto",
    "Corto vencimiento",
    "Otro",
]

ESTADOS_TICKET = [
    "Ticket generado",
    "Pendiente recepción física",
    "Mercadería recepcionada",
    "Control físico realizado",
    "Clasificación final",
    "SAP actualizado",
    "WMS actualizado",
    "Ticket cerrado",
]

tickets = []


def pausar():
    input("\nPresione ENTER para continuar...")


def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("Error: el dato no puede quedar vacío.")


def pedir_entero(mensaje, minimo=1):
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero >= minimo:
                return numero
            print(f"Error: ingrese un número mayor o igual a {minimo}.")
        except ValueError:
            print("Error: debe ingresar un número válido.")


def elegir_opcion(lista, titulo):
    print(f"\n{titulo}")
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item}")

    while True:
        opcion = pedir_entero("Seleccione una opción: ", 1)
        if 1 <= opcion <= len(lista):
            return lista[opcion - 1]
        print("Error: opción inexistente.")


def generar_id_ticket():
    return f"TK-{len(tickets) + 1:04d}"


def buscar_ticket(id_ticket):
    for ticket in tickets:
        if ticket["id_ticket"].upper() == id_ticket.upper():
            return ticket
    return None


def mostrar_resumen_ticket(ticket):
    print("\n" + "=" * 60)
    print(f"TICKET: {ticket['id_ticket']}")
    print(f"Fecha aviso: {ticket['fecha_aviso']}")
    print(f"Delivery: {ticket['delivery']}")
    print(f"Cliente: {ticket['cliente']}")
    print(f"Estado ticket: {ticket['estado_ticket']}")
    print(f"EDI: {ticket['edi'] if ticket['edi'] else 'Pendiente'}")
    print(f"SAP: {ticket['estado_sap']}")
    print(f"WMS: {ticket['estado_wms']}")
    print("-" * 60)
    print("Ítems del rechazo:")

    for i, item in enumerate(ticket["items"], start=1):
        print(f"\nItem {i}")
        print(f"  SKU: {item['sku']} - {item['descripcion']}")
        print(f"  Lote: {item['lote']}")
        print(f"  Vencimiento: {item['vencimiento']}")
        print(f"  Cantidad: {item['cantidad']}")
        print(f"  Motivo inicial: {item['motivo_inicial']}")
        print(f"  Motivo final: {item['motivo_final']}")
        print(f"  Estado físico: {item['estado_fisico']}")
        print(f"  Clasificación: {item['clasificacion']}")
    print("=" * 60)


def registrar_ticket():
    print("\n--- REGISTRAR NUEVO TICKET DE RECHAZO ---")

    delivery = pedir_texto("Ingrese número de delivery: ")
    cliente = pedir_texto("Ingrese cliente: ")
    cantidad_items = pedir_entero("¿Cuántos ítems tiene el rechazo?: ", 1)

    items = []

    for numero_item in range(1, cantidad_items + 1):
        print(f"\n--- Carga del item {numero_item} ---")

        while True:
            sku = pedir_texto("Ingrese SKU: ")
            if sku in PRODUCTOS:
                descripcion = PRODUCTOS[sku]
                print(f"Producto encontrado: {descripcion}")
                break
            print("SKU inexistente en la base simulada.")
            print("SKUs disponibles para prueba:", ", ".join(PRODUCTOS.keys()))

        lote = pedir_texto("Ingrese lote: ")
        vencimiento = pedir_texto("Ingrese fecha de vencimiento (ej. 12/2026): ")
        cantidad = pedir_entero("Ingrese cantidad rechazada: ", 1)
        motivo_inicial = elegir_opcion(MOTIVOS, "Seleccione motivo inicial informado")
        estado_fisico = elegir_opcion(["Sana", "Rota"], "Seleccione estado físico informado")

        item = {
            "sku": sku,
            "descripcion": descripcion,
            "lote": lote,
            "vencimiento": vencimiento,
            "cantidad": cantidad,
            "motivo_inicial": motivo_inicial,
            "motivo_final": "Pendiente control CDM",
            "estado_fisico": estado_fisico,
            "clasificacion": "Pendiente",
        }

        items.append(item)

    ticket = {
        "id_ticket": generar_id_ticket(),
        "fecha_aviso": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "delivery": delivery,
        "cliente": cliente,
        "items": items,
        "estado_ticket": "Ticket generado",
        "edi": "",
        "estado_sap": "Pendiente",
        "estado_wms": "Pendiente",
    }

    tickets.append(ticket)

    print("\nTicket generado correctamente.")
    print(f"Número de ticket: {ticket['id_ticket']}")
    print("Estado inicial: Ticket generado")


def consultar_ticket():
    print("\n--- CONSULTAR TICKET ---")
    id_ticket = pedir_texto("Ingrese ID de ticket (ej. TK-0001): ")
    ticket = buscar_ticket(id_ticket)

    if ticket is None:
        print("No se encontró el ticket solicitado.")
        return

    mostrar_resumen_ticket(ticket)


def mostrar_tickets():
    print("\n--- LISTADO DE TICKETS ---")

    if not tickets:
        print("No hay tickets registrados.")
        return

    for ticket in tickets:
        print(
            f"{ticket['id_ticket']} | Delivery: {ticket['delivery']} | "
            f"Cliente: {ticket['cliente']} | Estado: {ticket['estado_ticket']} | "
            f"Ítems: {len(ticket['items'])}"
        )


def actualizar_estado():
    print("\n--- ACTUALIZAR ESTADO DEL TICKET ---")
    id_ticket = pedir_texto("Ingrese ID de ticket: ")
    ticket = buscar_ticket(id_ticket)

    if ticket is None:
        print("No se encontró el ticket solicitado.")
        return

    nuevo_estado = elegir_opcion(ESTADOS_TICKET[:-1], "Seleccione nuevo estado")

    ticket["estado_ticket"] = nuevo_estado
    print(f"Estado actualizado a: {nuevo_estado}")

    if nuevo_estado == "Control físico realizado":
        actualizar_control_fisico(ticket)

    if nuevo_estado == "SAP actualizado":
        actualizar_sap(ticket)

    if nuevo_estado == "WMS actualizado":
        actualizar_wms(ticket)


def actualizar_control_fisico(ticket):
    print("\n--- CONTROL FÍSICO CDM ---")
    print("Durante esta etapa se puede modificar el motivo final y la clasificación de cada ítem.")

    for i, item in enumerate(ticket["items"], start=1):
        print(f"\nItem {i}: SKU {item['sku']} - Lote {item['lote']}")

        motivo_final = elegir_opcion(MOTIVOS, "Seleccione motivo final determinado por CDM")
        estado_fisico = elegir_opcion(["Sana", "Rota"], "Seleccione estado físico final")
        clasificacion = elegir_opcion(["Apta", "No apta"], "Seleccione clasificación final")

        item["motivo_final"] = motivo_final
        item["estado_fisico"] = estado_fisico
        item["clasificacion"] = clasificacion

    ticket["estado_ticket"] = "Clasificación final"
    print("Control físico y clasificación final registrados.")


def actualizar_sap(ticket):
    print("\n--- ACTUALIZACIÓN SAP ---")
    edi = pedir_texto("Ingrese número EDI generado por SAP: ")
    ticket["edi"] = edi

    hay_no_aptos = any(item["clasificacion"] == "No apta" for item in ticket["items"])

    if hay_no_aptos:
        ticket["estado_sap"] = "TC02 - Stock no apto para la venta"
    else:
        ticket["estado_sap"] = "TC01 - Stock apto para la venta"

    print(f"EDI registrado: {edi}")
    print(f"Estado SAP actualizado: {ticket['estado_sap']}")


def actualizar_wms(ticket):
    print("\n--- ACTUALIZACIÓN WMS ---")

    hay_no_aptos = any(item["clasificacion"] == "No apta" for item in ticket["items"])

    if hay_no_aptos:
        ticket["estado_wms"] = "SCP - Mercadería no apta para la venta"
    else:
        ticket["estado_wms"] = "AMU - Mercadería apta para la venta"

    print(f"Estado WMS actualizado: {ticket['estado_wms']}")


def cerrar_ticket():
    print("\n--- CERRAR TICKET ---")
    id_ticket = pedir_texto("Ingrese ID de ticket: ")
    ticket = buscar_ticket(id_ticket)

    if ticket is None:
        print("No se encontró el ticket solicitado.")
        return

    if not ticket["edi"]:
        print("No se puede cerrar el ticket: falta registrar EDI.")
        return

    if ticket["estado_sap"] == "Pendiente":
        print("No se puede cerrar el ticket: SAP aún no fue actualizado.")
        return

    if ticket["estado_wms"] == "Pendiente":
        print("No se puede cerrar el ticket: WMS aún no fue actualizado.")
        return

    ticket["estado_ticket"] = "Ticket cerrado"
    print("Ticket cerrado correctamente.")
    print("SAP y WMS se encuentran alineados.")


def menu():
    while True:
        print("\n" + "=" * 60)
        print("CHATBOT - GESTIÓN DE RECHAZOS LOGÍSTICOS")
        print("=" * 60)
        print("1. Registrar nuevo ticket")
        print("2. Consultar ticket")
        print("3. Actualizar estado del ticket")
        print("4. Mostrar todos los tickets")
        print("5. Cerrar ticket")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_ticket()
            pausar()
        elif opcion == "2":
            consultar_ticket()
            pausar()
        elif opcion == "3":
            actualizar_estado()
            pausar()
        elif opcion == "4":
            mostrar_tickets()
            pausar()
        elif opcion == "5":
            cerrar_ticket()
            pausar()
        elif opcion == "6":
            print("Finalizando chatbot. Hasta luego.")
            break
        else:
            print("Opción inválida. Ingrese un número del 1 al 6.")


if __name__ == "__main__":
    menu()
