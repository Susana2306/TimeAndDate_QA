# language: es
Característica: Escenario 013 - Contribuciones (HU-17)

  @RutaAlterna
  Escenario: Cancelación del flujo de contribución
    Dado que el usuario abre el formulario de contacto o feedback
    Cuando redacta un mensaje en el campo de descripción
    Y recarga la página o navega hacia atrás antes de enviarlo
    Entonces la contribución se descarta y el formulario vuelve a su estado vacío

  @RutaAlterna
  Escenario: Flujo completo de contribución
    Dado que el formulario de feedback está cargado
    Cuando el usuario ingresa su nombre, un correo válido y un mensaje de prueba
    Y hace clic en enviar
    Entonces se muestra una pantalla o mensaje de confirmación de recepción del mensaje
