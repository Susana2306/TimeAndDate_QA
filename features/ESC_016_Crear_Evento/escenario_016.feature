# language: es
Característica: Escenario 016 - Crear evento y visualizar cuenta regresiva (HU-2)

  @RutaCritica @I-2.1
  Escenario: Creación de evento visible en calendario
    Dado que el usuario está en el creador de cuenta regresiva
    Cuando llena los detalles del evento con fecha futura
    Y hace clic en "Create Countdown"
    Entonces se genera una URL única que muestra el cronómetro en vivo hacia la fecha del evento
