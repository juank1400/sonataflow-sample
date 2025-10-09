# CNCF Workflow implementation

## Implementando un workflow con SonataFlow

Este repositorio contiene una implementación de un flujo de trabajo (workflow) utilizando SonataFlow. El ejemplo principal es una saga para la reserva de un tour.

### Proyecto: Saga de Reserva de Tour (`tour_reservation_saga`)

Este proyecto demuestra cómo orquestar servicios (vuelos, hoteles) usando el patrón de saga para garantizar la consistencia de los datos.

#### Prerrequisitos

*   Java (versión compatible con Quarkus)
*   Maven o Gradle
*   Docker (o Podman) para ejecutar los servicios dependientes.

#### Cómo ejecutar

Para ejecutar el proyecto, navega al directorio `tour_reservation_saga` y sigue las instrucciones que encontrarás en su propio `README.md` (una vez que lo crees). Típicamente, para un proyecto Quarkus, los pasos serían:
1.  Iniciar los servicios externos (por ejemplo, con Docker Compose).
2.  Ejecutar la aplicación Quarkus en modo de desarrollo.
