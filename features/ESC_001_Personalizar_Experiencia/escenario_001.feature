# language: es
Característica: Escenario 001 - Personalizar experiencia de usuario (HU-1)

  @RutaCritica
  Escenario: Inicio de sesión y personalización de perfil
    Dado que el usuario abre la página principal de timeanddate.com
    Cuando hace clic en el enlace de "Sign In" en el header
    Y ingresa un correo y contraseña válidos
    Y presiona el botón de iniciar sesión
    Y navega a la sección de configuración "My Units" (/custom/)
    Y cambia la ciudad base a "Bogotá" y el idioma de la interfaz
    Y guarda los cambios de personalización
    Entonces el perfil se actualiza correctamente y las preferencias se guardan en la interfaz

  @RutaAlterna
  Escenario: Inicio de sesión fallido por credenciales inválidas
    Dado que el usuario está en la pantalla de inicio de sesión ("Sign In")
    Cuando ingresa un usuario no registrado o una contraseña incorrecta
    Y intenta acceder al sistema
    Entonces el sistema deniega el acceso y muestra un mensaje de error en el formulario

  @RutaAlterna
  Escenario: Validación de ciudad inválida
    Dado que el usuario se encuentra autenticado en su perfil
    Cuando va a la configuración de "My Units" e intenta buscar una ciudad inválida como "12345"
    Y guarda las modificaciones
    Entonces la ciudad inválida no se guarda y el reloj y clima mantienen la configuración anterior

  @RutaAlterna
  Escenario: Preferencias reflejadas en reloj y clima
    Dado que el usuario modificó exitosamente su ciudad base a "Bogotá" en sus preferencias
    Cuando navega por los diferentes módulos de la plataforma de timeanddate
    Entonces la ciudad configurada en preferencias se refleja automáticamente en las consultas de reloj mundial y clima