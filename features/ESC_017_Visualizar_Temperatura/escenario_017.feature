# language: es
Característica: Escenario 017 - Obtener Información Meteorológica (HU-3)

  @RutaAlterna @U-3.1
  Escenario: Visualización del valor de temperatura en clima
    Dado que el usuario ingresa a la sección principal del clima
    Cuando busca cualquier ciudad válida
    Entonces el panel de resultados muestra un valor numérico acompañado del símbolo "°C" o "°F"