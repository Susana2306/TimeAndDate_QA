# language: es
Característica: Escenario 014 - Consultar eventos y fechas importantes (HU-2)

  @RutaAlterna
  Escenario: Cancelación de creación de evento
    Dado que el usuario ingresa al creador de cuenta regresiva para un evento
    Cuando llena el título del evento con "Reunión GITESI"
    Y presiona el botón o enlace para cancelar o regresar al inicio
    Entonces el sistema regresa a la página anterior sin generar ni guardar la cuenta regresiva