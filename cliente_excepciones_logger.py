# =============================================================================
# MÓDULO: EXCEPCIONES PERSONALIZADAS, LOGGER Y CLASE CLIENTE
# Sistema Integral de Gestión - Empresa Software FJ
# Curso: Programación 213023 - UNAD | Fase 4
# Desarrollado por: SEBASTIAN CORRO
# =============================================================================
# Este módulo contiene:
#   1. Excepciones personalizadas del sistema
#   2. Sistema de registro de eventos (Logger)
#   3. Clase Cliente con encapsulación y validaciones estrictas
# =============================================================================


from abc import ABC, abstractmethod  # Necesario para heredar de EntidadSistema
import datetime                       # Para registrar fecha y hora en los logs
import os                             # Para operaciones con archivos


# =============================================================================
# SECCIÓN 1: EXCEPCIONES PERSONALIZADAS
# Permiten identificar con precisión qué tipo de error ocurrió en el sistema
# =============================================================================

class ErrorClienteInvalido(Exception):
    """
    Excepción personalizada que se lanza cuando los datos
    de un cliente no cumplen con las validaciones requeridas.
    Ejemplos: correo sin @, teléfono con letras, nombre vacío.
    """
    pass


class ErrorServicioNoDisponible(Exception):
    """
    Excepción personalizada que se lanza cuando se intenta
    usar un servicio que no está disponible en el sistema,
    o cuando sus parámetros de creación son inválidos.
    """
    pass


class ErrorReservaInvalida(Exception):
    """
    Excepción personalizada que se lanza cuando una reserva
    tiene datos incorrectos, o cuando se intenta realizar
    una operación no permitida sobre ella (ej: confirmar
    una reserva ya cancelada).
    """
    pass


class ErrorDuracionInvalida(Exception):
    """
    Excepción personalizada que se lanza cuando la duración
    indicada para una reserva no es válida (ej: 0 horas,
    horas negativas, o un valor no numérico).
    """
    pass


class ErrorCalculoCosto(Exception):
    """
    Excepción personalizada que se lanza cuando ocurre
    un error durante el cálculo del costo de un servicio,
    por ejemplo descuentos fuera de rango o impuestos negativos.
    """
    pass


# =============================================================================
# SECCIÓN 2: SISTEMA DE LOGS (LOGGER)
# Registra todos los eventos y errores en un archivo externo,
# manteniendo la aplicación activa ante cualquier fallo.
# =============================================================================

class Logger:
    """
    Clase utilitaria para registrar eventos del sistema en un archivo de log.

    Características:
    - Guarda cada evento con fecha y hora exacta
    - También muestra el evento en consola para seguimiento en tiempo real
    - Si no puede escribir el archivo, avisa pero NO detiene el sistema
    - Usa try/finally para garantizar el cierre del archivo siempre
    """

    # Nombre del archivo donde se guardarán todos los registros
    ARCHIVO_LOG = "eventos_software_fj.log"

    @staticmethod
    def registrar(tipo, mensaje):
        """
        Registra un evento en el archivo de log.

        Parámetros:
            tipo (str): Categoría del evento. Puede ser:
                        'INFO'        → operación exitosa
                        'ERROR'       → fallo capturado
                        'ADVERTENCIA' → situación inusual pero no crítica
            mensaje (str): Descripción detallada del evento ocurrido.

        Manejo de excepciones:
            - Usa try/finally para asegurar que el archivo
              siempre se cierre aunque ocurra un error al escribir.
        """
        archivo = None  # Se inicializa en None para el bloque finally
        try:
            # Obtener la fecha y hora actual con formato legible
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Construir la línea que se escribirá en el archivo
            linea = f"[{timestamp}] [{tipo}] {mensaje}\n"

            # Abrir el archivo en modo 'append' para no borrar registros anteriores
            archivo = open(Logger.ARCHIVO_LOG, "a", encoding="utf-8")
            archivo.write(linea)

            # Mostrar también en consola para seguimiento inmediato
            print(f"  📋 LOG {tipo}: {mensaje}")

        except OSError as e:
            # Si hay un error de sistema de archivos, se avisa sin detener la app
            print(f"  ⚠️  No se pudo escribir en el log: {e}")

        finally:
            # El bloque finally SIEMPRE se ejecuta: cierra el archivo si fue abierto
            if archivo:
                archivo.close()


# =============================================================================
# SECCIÓN 3: CLASE ABSTRACTA BASE
# Define la estructura común de todas las entidades del sistema.
# Se importa aquí para que Cliente pueda heredar de ella.
# =============================================================================

class EntidadSistema(ABC):
    """
    Clase abstracta base del sistema Software FJ.
    Todas las entidades principales (Cliente, Servicio) deben heredar de esta clase.

    Obliga a implementar el método describir(), garantizando que
    todas las entidades puedan presentar su información de forma estándar.
    """

    @abstractmethod
    def describir(self):
        """
        Método abstracto que cada clase hija debe implementar.
        Debe retornar una cadena con la descripción de la entidad.
        """
        pass

    def __str__(self):
        """
        Permite usar print(objeto) directamente.
        Llama al método describir() de cada clase hija.
        """
        return self.describir()


# =============================================================================
# SECCIÓN 4: CLASE CLIENTE
# Gestiona los datos personales con encapsulación (atributos privados)
# y validaciones estrictas en cada campo.
# =============================================================================

class Cliente(EntidadSistema):
    """
    Representa un cliente registrado en el sistema de Software FJ.

    Principios aplicados:
    - ENCAPSULACIÓN: Los atributos son privados (prefijo _).
      Solo se accede a ellos mediante @property (getters).
    - HERENCIA: Hereda de EntidadSistema e implementa describir().
    - VALIDACIÓN: Cada dato se valida antes de ser asignado.
      Si es inválido, se lanza ErrorClienteInvalido.

    Atributos privados:
        _nombre     (str): Nombre completo del cliente
        _correo     (str): Correo electrónico válido
        _telefono   (str): Número de teléfono (solo dígitos)
        _id_cliente (int): Identificador único positivo
        _activo    (bool): Estado del cliente en el sistema
    """

    def __init__(self, nombre, correo, telefono, id_cliente):
        """
        Constructor del cliente.
        Valida todos los campos antes de crear el objeto.

        Parámetros:
            nombre     (str): Nombre del cliente (mínimo 2 caracteres)
            correo     (str): Correo electrónico (debe contener @ y .)
            telefono   (str/int): Teléfono (entre 7 y 15 dígitos numéricos)
            id_cliente (int): ID único del cliente (entero positivo)

        Lanza:
            ErrorClienteInvalido: Si alguno de los campos no es válido.
        """
        # Cada campo pasa por su método de validación antes de asignarse
        self._nombre     = self._validar_nombre(nombre)
        self._correo     = self._validar_correo(correo)
        self._telefono   = self._validar_telefono(telefono)
        self._id_cliente = self._validar_id(id_cliente)
        self._activo     = True  # Todo cliente nuevo empieza activo

        # Se registra la creación exitosa en el log
        Logger.registrar(
            "INFO",
            f"Cliente creado exitosamente: {self._nombre} (ID: {self._id_cliente})"
        )

    # -------------------------------------------------------------------------
    # Métodos privados de validación
    # Solo se usan dentro de la clase, no son accesibles desde afuera
    # -------------------------------------------------------------------------

    def _validar_nombre(self, nombre):
        """
        Valida que el nombre sea una cadena con al menos 2 caracteres.

        Lanza ErrorClienteInvalido si el nombre está vacío o es muy corto.
        """
        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise ErrorClienteInvalido(
                "El nombre debe ser texto y tener al menos 2 caracteres."
            )
        return nombre.strip()  # Se retorna sin espacios al inicio/fin

    def _validar_correo(self, correo):
        """
        Valida que el correo tenga formato básico: debe contener '@' y '.'.

        Lanza ErrorClienteInvalido si el formato no es válido.
        """
        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise ErrorClienteInvalido(
                f"El correo '{correo}' no tiene un formato válido. "
                f"Debe contener '@' y '.'."
            )
        return correo.strip().lower()  # Se guarda en minúsculas y sin espacios

    def _validar_telefono(self, telefono):
        """
        Valida que el teléfono sea numérico y tenga entre 7 y 15 dígitos.
        Acepta guiones y espacios que luego elimina.

        Lanza ErrorClienteInvalido si el formato es inválido.
        """
        # Eliminar espacios y guiones para quedarse solo con dígitos
        tel_str = str(telefono).replace(" ", "").replace("-", "")

        if not tel_str.isdigit() or not (7 <= len(tel_str) <= 15):
            raise ErrorClienteInvalido(
                f"El teléfono '{telefono}' no es válido. "
                f"Debe contener entre 7 y 15 dígitos numéricos."
            )
        return tel_str

    def _validar_id(self, id_cliente):
        """
        Valida que el ID sea un número entero positivo.

        Lanza ErrorClienteInvalido si el ID es inválido.
        """
        if not isinstance(id_cliente, int) or id_cliente <= 0:
            raise ErrorClienteInvalido(
                f"El ID '{id_cliente}' debe ser un número entero positivo."
            )
        return id_cliente

    # -------------------------------------------------------------------------
    # Getters con @property
    # Permiten leer los atributos privados sin modificarlos directamente
    # -------------------------------------------------------------------------

    @property
    def nombre(self):
        """Retorna el nombre del cliente."""
        return self._nombre

    @property
    def correo(self):
        """Retorna el correo del cliente."""
        return self._correo

    @property
    def telefono(self):
        """Retorna el teléfono del cliente."""
        return self._telefono

    @property
    def id_cliente(self):
        """Retorna el ID del cliente."""
        return self._id_cliente

    @property
    def activo(self):
        """Retorna True si el cliente está activo, False si fue desactivado."""
        return self._activo

    # -------------------------------------------------------------------------
    # Métodos públicos
    # -------------------------------------------------------------------------

    def desactivar(self):
        """
        Desactiva al cliente en el sistema.
        Un cliente inactivo no puede hacer nuevas reservas.
        """
        self._activo = False
        Logger.registrar("INFO", f"Cliente desactivado: {self._nombre} (ID: {self._id_cliente})")

    def describir(self):
        """
        Implementación del método abstracto de EntidadSistema.
        Retorna una descripción completa del cliente en una sola línea.
        """
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente ID {self._id_cliente}: {self._nombre} | "
            f"Correo: {self._correo} | "
            f"Tel: {self._telefono} | "
            f"Estado: {estado}"
        )


# =============================================================================
# BLOQUE DE PRUEBA
# Se ejecuta solo cuando se corre este archivo directamente.
# Sirve para verificar que el módulo funciona de forma independiente.
# =============================================================================

if __name__ == "__main__":

    print("\n" + "="*60)
    print("  PRUEBA DEL MÓDULO: Cliente, Excepciones y Logger")
    print("="*60)

    # --- Prueba 1: Cliente válido ---
    print("\n✅ PRUEBA 1: Crear cliente con datos válidos")
    try:
        c1 = Cliente("Ana Martínez", "ana.martinez@email.com", "3001234567", 1)
        print(f"  {c1.describir()}")
    except ErrorClienteInvalido as e:
        print(f"  ❌ Error inesperado: {e}")

    # --- Prueba 2: Correo inválido ---
    print("\n❌ PRUEBA 2: Cliente con correo inválido")
    try:
        c2 = Cliente("Pedro Malo", "pedrosinEmail.com", "3009876543", 2)
    except ErrorClienteInvalido as e:
        print(f"  Error capturado correctamente: {e}")
        Logger.registrar("ERROR", f"Correo inválido rechazado: {e}")

    # --- Prueba 3: Teléfono inválido ---
    print("\n❌ PRUEBA 3: Cliente con teléfono inválido")
    try:
        c3 = Cliente("María Letras", "maria@email.com", "abcdefg", 3)
    except ErrorClienteInvalido as e:
        print(f"  Error capturado correctamente: {e}")
        Logger.registrar("ERROR", f"Teléfono inválido rechazado: {e}")

    # --- Prueba 4: ID inválido ---
    print("\n❌ PRUEBA 4: Cliente con ID negativo")
    try:
        c4 = Cliente("Juan Negativo", "juan@email.com", "3112223344", -5)
    except ErrorClienteInvalido as e:
        print(f"  Error capturado correctamente: {e}")
        Logger.registrar("ERROR", f"ID inválido rechazado: {e}")

    # --- Prueba 5: Desactivar cliente ---
    print("\n🔴 PRUEBA 5: Desactivar un cliente")
    try:
        c5 = Cliente("Laura Gómez", "lgomez@empresa.co", "6054445566", 5)
        print(f"  Antes: {c5.describir()}")
        c5.desactivar()
        print(f"  Después: {c5.describir()}")
    except ErrorClienteInvalido as e:
        print(f"  ❌ Error inesperado: {e}")

    print("\n" + "="*60)
    print(f"  Revisa el archivo '{Logger.ARCHIVO_LOG}' para ver todos los registros.")
    print("="*60 + "\n")
