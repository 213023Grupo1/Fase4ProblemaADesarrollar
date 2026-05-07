from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import Dict, List

# =========================================================
# CONFIGURACIÓN
# =========================================================
logging.basicConfig(
    filename='software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# =========================================================
# EXCEPCIONES
# =========================================================
class SoftwareFJError(Exception): pass
class ClienteNoEncontradoError(SoftwareFJError): pass
class ClienteDuplicadoError(SoftwareFJError): pass
class ServicioInvalidoError(SoftwareFJError): pass
class ReservaError(SoftwareFJError): pass

# =========================================================
# SERVICIOS
# =========================================================
class Servicio(ABC):
    def __init__(self, nombre: str, precio_base: float):
        if precio_base <= 0:
            raise ServicioInvalidoError("El precio base debe ser positivo")
        self._nombre = nombre
        self._precio_base = precio_base

    @abstractmethod
    def calcular_precio(self) -> float:
        pass

    @property
    def nombre(self):
        return self._nombre

    def __str__(self):
        return f"{self._nombre} (${self._precio_base})"


class Sala(Servicio):
    def __init__(self, nombre: str, precio_base: float, horas: int):
        super().__init__(nombre, precio_base)
        if horas <= 0:
            raise ServicioInvalidoError("Las horas deben ser positivas")
        self.horas = horas

    def calcular_precio(self) -> float:
        return self._precio_base * self.horas


class Equipo(Servicio):
    DESCUENTO = 0.1

    def __init__(self, nombre: str, precio_base: float, dias: int):
        super().__init__(nombre, precio_base)
        if dias <= 0:
            raise ServicioInvalidoError("Los días deben ser positivos")
        self.dias = dias

    def calcular_precio(self) -> float:
        total = self._precio_base * self.dias
        if self.dias > 5:
            total *= (1 - self.DESCUENTO)
        return total


class Asesoria(Servicio):
    def __init__(self, nombre: str, precio_base: float, nivel: int):
        super().__init__(nombre, precio_base)
        if nivel not in (1, 2, 3):
            raise ServicioInvalidoError("Nivel debe ser 1, 2 o 3")
        self.nivel = nivel

    def calcular_precio(self) -> float:
        return self._precio_base * self.nivel

# =========================================================
# ENTIDADES
# =========================================================
class Cliente:
    def __init__(self, id_cliente: str, nombre: str, email: str):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email

    def __str__(self):
        return f"{self.nombre} (ID: {self.id_cliente})"


class Reserva:
    _contador = 1

    def __init__(self, cliente: Cliente, servicio: Servicio):
        self.id_reserva = Reserva._contador
        Reserva._contador += 1

        self.cliente = cliente
        self.servicio = servicio
        self.fecha = datetime.now()

    def detalle(self) -> str:
        return (
            f"ID: {self.id_reserva}\n"
            f"Fecha: {self.fecha.strftime('%d/%m/%Y %H:%M')}\n"
            f"Cliente: {self.cliente}\n"
            f"Servicio: {self.servicio}\n"
            f"Total: ${self.servicio.calcular_precio():.2f}"
        )

# =========================================================
# LÓGICA DE NEGOCIO
# =========================================================
class SoftwareFJ:
    def __init__(self):
        self._clientes: Dict[str, Cliente] = {}
        self._reservas: List[Reserva] = []

    # ---------- CLIENTES ----------
    def registrar_cliente(self, id_c: str, nombre: str, email: str):
        if id_c in self._clientes:
            raise ClienteDuplicadoError(f"El cliente {id_c} ya existe")

        cliente = Cliente(id_c, nombre, email)
        self._clientes[id_c] = cliente
        logging.info(f"Cliente registrado: {cliente}")
        return cliente

    def obtener_cliente(self, id_c: str) -> Cliente:
        if id_c not in self._clientes:
            raise ClienteNoEncontradoError(f"Cliente {id_c} no encontrado")
        return self._clientes[id_c]

    # ---------- RESERVAS ----------
    def crear_reserva(self, id_cliente: str, servicio: Servicio) -> Reserva:
        cliente = self.obtener_cliente(id_cliente)

        reserva = Reserva(cliente, servicio)
        self._reservas.append(reserva)

        logging.info(f"Reserva creada: {reserva.id_reserva}")
        return reserva

    def listar_reservas(self) -> List[Reserva]:
        return list(self._reservas)

# =========================================================
# INTERFAZ (CLI LIMPIO)
# =========================================================
class CLI:
    def __init__(self):
        self.app = SoftwareFJ()

    def ejecutar(self):
        while True:
            print("\n--- SISTEMA SOFTWARE FJ ---")
            print("1. Registrar Cliente")
            print("2. Nueva Reserva")
            print("3. Ver Reservas")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            try:
                if opcion == "1":
                    self.registrar_cliente()
                elif opcion == "2":
                    self.crear_reserva()
                elif opcion == "3":
                    self.ver_reservas()
                elif opcion == "4":
                    print("Saliendo...")
                    break
                else:
                    print("Opción inválida")

            except SoftwareFJError as e:
                print(f"⚠️ {e}")
                logging.warning(e)
            except ValueError:
                print("❌ Entrada inválida")
            except Exception as e:
                print("🔥 Error crítico")
                logging.error(e, exc_info=True)

    def registrar_cliente(self):
        id_c = input("ID: ")
        nombre = input("Nombre: ")
        email = input("Email: ")

        cliente = self.app.registrar_cliente(id_c, nombre, email)
        print(f"✅ Cliente registrado: {cliente}")

    def crear_reserva(self):
        id_c = input("ID Cliente: ")

        print("1. Sala | 2. Equipo | 3. Asesoría")
        tipo = input("Seleccione: ")

        servicio = self._crear_servicio(tipo)
        reserva = self.app.crear_reserva(id_c, servicio)

        print("\n🚀 Reserva creada")
        print(reserva.detalle())

    def ver_reservas(self):
        reservas = self.app.listar_reservas()

        if not reservas:
            print("No hay reservas")
            return

        for r in reservas:
            print("\n" + r.detalle())
            print("-" * 30)

    def _crear_servicio(self, tipo: str) -> Servicio:
        if tipo == "1":
            horas = int(input("Horas: "))
            return Sala("Sala", 50, horas)

        elif tipo == "2":
            dias = int(input("Días: "))
            return Equipo("Equipo", 30, dias)

        elif tipo == "3":
            nivel = int(input("Nivel (1-3): "))
            return Asesoria("Asesoría", 100, nivel)

        else:
            raise ServicioInvalidoError("Tipo de servicio inválido")

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    CLI().ejecutar()
