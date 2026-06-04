# language: es
Característica: Escenario 027 - Calcular duraciones y planificación de fechas (HU-9)

  @RutaAlterna
  Escenario: Validación de formato incorrecto en fechas
    Dado que el usuario abre la calculadora de fechas de timeanddate
    Cuando ingresa un valor de mes inválido como "15" en la fecha de inicio
    Y hace clic en el botón de calcular duración
    Entonces el sistema muestra un mensaje de error indicando que la fecha es inválida y no calcula el resultado

  @RutaAlterna
  Escenario: Cálculo con fechas válidas
    Dado que el usuario abre la calculadora de fechas
    Cuando ingresa "1 de Enero de 2025" como fecha de inicio
    Y ingresa "1 de Enero de 2026" como fecha de fin
    Y hace clic en el botón de calcular duración
    Entonces el resultado muestra exactamente "365 days" o su equivalente