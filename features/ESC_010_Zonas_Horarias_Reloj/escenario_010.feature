# language: es
Característica: Escenario 010 - Calcular zonas horarias y consultar reloj mundial (HU-14 / HU-13)

  @RutaCritica @E-4.1
  Escenario: Conversión de hora y contraste con reloj mundial
    Dado que el usuario convierte la hora actual de Bogotá a "Tokio" en el conversor de husos horarios
    Cuando anota el resultado de la conversión
    Y navega inmediatamente al "World Clock" y busca "Tokio"
    Entonces la hora mostrada en el reloj mundial para Tokio coincide con la conversión previa con un margen máximo de 1 minuto