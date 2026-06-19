# TPI Organización Empresarial — Chatbot de Gestión de Rechazos Logísticos

Trabajo Práctico Integrador de la cátedra **Organización Empresarial**, Tecnicatura
Universitaria en Programación a Distancia (TUPaD) — UTN.

## ¿Qué hace el sistema?

Simula, mediante un chatbot por consola escrito en Python, el proceso administrativo
de **gestión de rechazos de mercadería** en un centro de distribución logístico: desde
que el transporte avisa una devolución hasta que esa devolución queda cerrada y
alineada en los sistemas SAP y WMS.

El chatbot permite:

- Registrar tickets de rechazo con uno o varios ítems (productos, lotes, motivos).
- Consultar el estado de un ticket.
- Avanzar el ticket a través de una máquina de estados (8 estados posibles).
- Registrar el control físico realizado por el Centro de Distribución (CDM), que
  puede confirmar o modificar el motivo y la clasificación informados inicialmente.
- Generar el número EDI y actualizar el estado en SAP (TC01/TC02) y en WMS (AMU/SCP).
- Cerrar el ticket una vez que todo quedó alineado.

## ¿Por qué este proceso?

La gestión de rechazos suele manejarse hoy por teléfono, mail y remitos sueltos, lo
que dificulta el seguimiento de cada caso y la sincronización entre lo que pasa
físicamente con la mercadería y lo que queda registrado en los sistemas. El chatbot
no reemplaza a SAP ni a WMS: actúa como capa de seguimiento y control sobre ese
proceso, asegurando que cada devolución se trate de punta a punta.

## Tecnologías utilizadas

- **Python 3** (sin librerías externas) — simulación por consola.
- **BPMN 2.0** — modelado del proceso de negocio (as-is / to-be).
- Herramientas de IA (ChatGPT, Claude) como apoyo en redacción y generación de ideas, bajo
  revisión y validación de los autores.

## Estructura del repositorio

```
TPI_Organizacion_Empresarial/
├── README.md
├── /chatbot
│   ├── chatbot_rechazos.py
│   └──/CSV_permanentes
│      ├── README_CSV.txt
│      ├── clientes.csv 
│      ├── detalle_rechazos.csv
│      ├── productos.csv
│      └── ticket.csv   
├── /documentacion
│   ├──Anexo Capturas IA.pdf
│   ├── Informe.pdf
│   ├── Manual_Usuario.md
│   ├── Casos_de_Prueba.md
│   └── BPMN OE.jpg
└── .gitignore
```

## Cómo ejecutarlo

Requiere Python 3.8 o superior (no usa librerías externas).

```bash
git clone <url-del-repositorio>
cd TPI_Organizacion_Empresarial/chatbot
python3 chatbot_rechazos.py
```

Al ejecutarlo se muestra un menú interactivo con 6 opciones: registrar ticket,
consultar ticket, actualizar estado, mostrar todos los tickets, cerrar ticket y
salir. Ver `documentacion/Manual_Usuario.md` para el detalle paso a paso.

## Seguridad y privacidad

El proyecto utiliza datos simulados y no contiene información confidencial real de clientes, productos ni operaciones comerciales. No se incluyen usuarios, contraseñas, tokens, claves de API ni credenciales de acceso a sistemas externos.

El chatbot no se conecta realmente a SAP ni a WMS; la integración es conceptual y se representa mediante estados simulados. Los archivos CSV utilizados funcionan como almacenamiento académico para demostrar persistencia de datos.

Se incorpora un archivo `.gitignore` para evitar subir archivos temporales, entornos virtuales, cachés o posibles archivos de configuración local.

## Equipo

| Integrante | Rol principal |
|---|---|
| Rodolfo Gutiérrez | Relevamiento del proceso operativo, diseño funcional, desarrollo del chatbot |
| Lucía Gutiérrez | Análisis funcional, validación de datos, documentación técnica, testing, administración del repositorio |

## Cátedra

Organización Empresarial — Prof. Gabriela Martínez (titular); Prof. Carolina Bruno,
Prof. Mario Raúl López, Prof. Andrea Ramos (adjuntos).
