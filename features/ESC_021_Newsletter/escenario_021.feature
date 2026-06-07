# language: es
Característica: Escenario 021 - Suscripción a Newsletter Informativo (HU-6)

  @RutaAlterna @U-6.2
  Escenario: Validación de formato incorrecto en newsletter
    Dado que el usuario se encuentra en la sección de Newsletter de la empresa (/news/newsletter.html)
    Cuando digita un correo con formato inválido como "kevin_sin_arroba.com"
    Y hace clic en el botón de suscripción "Subscribe"
    Entonces el sistema bloquea el envío y muestra un elemento de error de formato en el DOM

  @RutaAlterna @U-6.1
  Escenario: Validación de correo válido en newsletter
    Dado que el formulario de suscripción está desplegado en pantalla
    Cuando el usuario localiza el campo de entrada de texto para el email
    Y digita un correo electrónico estructurado correctamente
    Entonces la interfaz valida de forma preliminar y el mensaje de confirmación inicial se vuelve visible en el DOM

  @RutaAlterna @I-6.2
  Escenario: Validación de campo requerido en newsletter
    Dado que el usuario visualiza el campo de email del newsletter
    Cuando deja el campo de email completamente vacío o borra su contenido
    Y presiona el botón para enviar la suscripción
    Entonces se muestra un mensaje en pantalla indicando que es un campo requerido y no genera confirmación de éxito

  @RutaAlterna @I-6.1
  Escenario: Suscripción exitosa al newsletter
    Dado que el usuario está en la sección informativa de la empresa
    Cuando ingresa una dirección de correo válida y nueva que no esté registrada previamente
    Y confirma el envío del formulario
    Entonces el sistema procesa la solicitud y un elemento de confirmación final de suscripción exitosa es visible en el DOM