# CNCF Workflow implementation

## Implementando un workflow con SonataFlow

Este repositorio contiene una implementación de un flujo de trabajo (workflow) utilizando SonataFlow. El ejemplo principal es una saga para la reserva de un tour.

### Proyecto: Saga de Reserva de Tour (`tour_reservation_saga`)

Este proyecto demuestra cómo orquestar servicios (vuelos, hoteles) usando el patrón de saga para garantizar la consistencia de los datos. En esta primera versión todas las pruebas se llevarán a cabo en un entorno local. Donde se requieren algunos componentes instalados previamente.

#### Prerrequisitos

* Docker (o Podman) para ejecutar los servicios dependientes.
* Knative cli instalado y configurado
* kn_workflow desde SonataFlow, preferiblemente integrado con knative
* Un IDE de desarrollo suele ser suficiente, sin embargo, para poder vizualizar el flujo de trabajo mientras se desarrolla se puede usar la extensión de KIE server de VS Code.

#### Construcción del proyecto

Una vez instalados los prerequisitos SontaFlow kn_workflow permite construir un proyecto base usando la siguiente línea de comando:

```bash
kn workflow create --name tour_reservation_saga --yaml-workflow tour_reservation_saga/workflow.sw.yaml
```

Esta comando crea un proyecto en blanco para iniciar el desarrollo

Una vez creado el proyecto, se puede probar la versión inicial por medio del siguiente comando:

```bash
kn workflow run
```

Este iniciará un contenedor de sonataflow con el proyecto base desplegado sobre Quarkus que habilitará la interfaz de desarrollo de Quarkus con las respectivas extensiones de SonataFlow (Workflows). normalmente en http://localhost:8080/q/dev

#### Preparar el ambiente para probar el proyecto

Vamos a implementar un primer nivel, haremos que un llamado al workflow invoque a dos microservicios uno que reserve un vuelo y otro que reserve un hotel.

Para este fin, es posible implementar el proyecto qaurkus-rest-app que es un mock, para los micros de vuelos y hoteles.

Cuando se ejecuta esta aplicación deberá ejecutarse en http://localhost:8082/ y la especificación de la API, se encuentra en el archivo anexo openapi.json

#### Implementación del flujo de trabajo

Para implementar el proyecto usaremos el siguiente manifiesto en yaml usando la sintaxis de SonataFlow:

```yaml

id: TourReservationSaga
name: Reserva de Plan Turístico Concurrente y Compensación
version: "1.0"
specVersion: "0.8"
start: ProcesoReserva

# 1. Definición de Funciones (Servicios REST externos)

# ------------------------------------------------------------------

functions:

# Servicio de Vuelos

- name: reserveFlightFunction
  operation: "openapi.json#reserveFlight" # Apunta a openapi.json y la operación reserveFlight

# Servicio de Hoteles

- name: reserveHotelFunction
  operation: "openapi.json#reserveHotel" # Apunta a openapi.json y la operación reserveHotel

# 2. Definición de Estados del Flujo

# ------------------------------------------------------------------

states:

# Estado de inicio que invoca la secuencia de reservas

- name: ProcesoReserva
  type: inject
  data:
  message: "Iniciando proceso de reserva"
  transition: ReservarVuelo

# C. ESTADOS DE OPERACIÓN (Reserva de Vuelo y Hotel)

# ------------------------------------------------------------------

- name: ReservarVuelo
  type: operation
  actions:

  - name: make_flight_reservation
    functionRef:
    refName: "reserveFlightFunction"
    arguments:
    body: # Usamos expresiones ${...} para acceder a los datos del workflow
    passengerName: "${.tripInfo.passengerName}"
    flightNumber: "${.tripInfo.flightNumber}"
    transition: ReservarHotel
- name: ReservarHotel
  type: operation
  actions:

  - name: make_hotel_reservation
    functionRef:
    refName: "reserveHotelFunction"
    arguments:
    body: # Usamos expresiones ${...} para acceder a los datos del workflow
    guestName: "${.tripInfo.passengerName}"
    hotelName: "${.tripInfo.hotelName}"
    transition: FlujoExitoso
- name: FlujoExitoso
  type: inject
  data:
  status: "COMPLETED_SUCCESSFULLY"
  message: "Reserva completada exitosamente. Vuelo y Hotel confirmados."
  end: true

```

#### Cómo ejecutar

Para ejecutar el proyecto, navega al directorio `tour_reservation_saga` y sigue las instrucciones que encontrarás en su propio `README.md` (una vez que lo crees). Típicamente, para un proyecto Quarkus, los pasos serían:

1. Iniciar los servicios externos (quarkus-rest-app).
2. Vuelva a ejecutar el workflow.

```bash
kn workflow run
```

En el http://localhost:8080/q/dev identifique la extensión de workflows, busque la definición de nuestro workflow y seleccione ejecutar usando este json como parametro:

```json
{
  "tripInfo": {
    "passengerName": "Juan Perez",
    "flightNumber": "IB6845",
    "hotelName": "Marriott"
  }
}
```

Una vez ejecutado debería poder ver el detalle de cada ejecución las variables y detalles de la ejecución.
