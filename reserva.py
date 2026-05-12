# ============================================================
# CLASE RESERVA
# ============================================================

from cliente_excepciones_logger import (
    ErrorReservaInvalida,
    ErrorDuracionInvalida,
    Logger
)


class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = self._validar_duracion(duracion)
        self.estado = "pendiente"

        Logger.registrar("INFO", f"Reserva creada para {cliente.nombre}")

    # -------------------------------
    # VALIDACIÓN
    # -------------------------------
    def _validar_duracion(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ErrorDuracionInvalida(
                "La duración debe ser un número positivo."
            )
        return duracion

    # -------------------------------
    # MÉTODOS DE ESTADO
    # -------------------------------
    def confirmar(self):
        if self.estado != "pendiente":
            raise ErrorReservaInvalida(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.estado = "confirmada"
        Logger.registrar("INFO", f"Reserva confirmada para {self.cliente.nombre}")

    def cancelar(self):
        if self.estado == "completada":
            raise ErrorReservaInvalida(
                "No se puede cancelar una reserva ya completada."
            )

        self.estado = "cancelada"
        Logger.registrar("INFO", f"Reserva cancelada para {self.cliente.nombre}")

    def completar(self):
        if self.estado != "confirmada":
            raise ErrorReservaInvalida(
                "Solo se pueden completar reservas confirmadas."
            )

        self.estado = "completada"
        Logger.registrar("INFO", f"Reserva completada para {self.cliente.nombre}")

    # -------------------------------
    # COSTO
    # -------------------------------
    def calcular_total(self):
        try:
            total = self.servicio.calcular_precio() * self.duracion
            return total
        except Exception as e:
            Logger.registrar("ERROR", str(e))
            raise

    # -------------------------------
    # REPRESENTACIÓN
    # -------------------------------
    def __str__(self):
        return (
            f"Reserva -> Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio._nombre} | "
            f"Estado: {self.estado}"
        )