# language: es
Característica: Escenario 009 - Consultar zonas horarias básicas (HU-14)

  @RutaAlterna
  Escenario: Validación con zona origen y destino iguales
    Dado que el usuario abre el convertidor de huso horario de timeanddate (/worldclock/converter.html)
    Cuando selecciona "Colombia - Bogotá" en el campo de ciudad origen
    Y selecciona la misma zona "Colombia - Bogotá" en el campo de ciudad destino
    Y ejecuta el cálculo de conversión presionando el botón "Convert time"
    Entonces el resultado muestra exactamente la misma hora o un mensaje indicando que las zonas son idénticas

  @RutaAlterna
  Escenario: Conversión hacia zona destino
    Dado que el usuario se encuentra en la pantalla del convertidor de hora
    Cuando selecciona una zona origen "Colombia - Bogotá" y una zona destino diferente como "Spain - Madrid"
    Y introduce una hora específica para la conversión
    Y ejecuta el cálculo de conversión
    Entonces el resultado final en pantalla corresponde exactamente a la hora calculada y convertida en la zona destino