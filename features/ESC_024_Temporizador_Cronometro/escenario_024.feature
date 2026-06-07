# language: es
Característica: Escenario 024 - Medir Tiempo con Temporizador y Cronómetro en Línea (HU-8)

  @RutaAlterna @U-8.3
  Escenario: Validación de temporizador en cero
    Dado que el usuario abre la herramienta de temporizador
    Cuando el tiempo está configurado en "00:00:00"
    Y presiona el botón de "Start"
    Entonces el sistema no inicia el conteo o muestra una alerta para ingresar un tiempo mayor a cero

  @RutaAlterna @U-8.1
  Escenario: Inicio y detención del cronómetro
    Dado que el usuario configura el temporizador en "00:05:00"
    Cuando presiona "Start"
    Y espera unos segundos y luego presiona "Pause"
    Entonces el tiempo se detiene correctamente en el valor transcurrido

  @RutaAlterna @U-8.2
  Escenario: Reinicio correcto del cronómetro
    Dado que el temporizador se encuentra pausado después de haber iniciado
    Cuando el usuario hace clic en el botón "Reset"
    Entonces el temporizador vuelve a su configuración inicial