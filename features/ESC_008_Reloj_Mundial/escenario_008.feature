# language: es
Característica: Escenario 008 - Verificar reloj mundial en línea (HU-13)

  @RutaAlterna @U-13.1
  Escenario: Verificación de actualización del reloj mundial
    Dado que el usuario navega al reloj mundial de timeanddate
    Cuando obtiene la hora actual para "Colombia - Bogotá"
    Y espera unos segundos
    Entonces la hora mostrada en el reloj se ha actualizado con respecto a la lectura anterior
