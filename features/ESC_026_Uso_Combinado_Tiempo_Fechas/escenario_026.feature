# language: es
Característica: Escenario 026 - Uso combinado de herramientas (HU-8 / HU-9)

  @RutaCritica @E-3.1
  Escenario: Uso combinado de temporizador y calculadora de fechas
    Dado que el usuario tiene abierto el temporizador en una pestaña
    Cuando inicia un contador de 10 minutos
    Y abre en otra pestaña la calculadora de fechas para verificar los días hasta fin de año
    Entonces el temporizador sigue ejecutándose en segundo plano sin interrumpirse por la consulta de fechas