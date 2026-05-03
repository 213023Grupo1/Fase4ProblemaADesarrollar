from abc import ABC, abstractmethod
from datetime import datetime

class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self._nombre = nombre
        self._precio_base = precio_base

    @abstractmethod
    def calcular_precio(self):
        pass
    
    def __str__(self):
            return f"Servicio: {self._nombre} | Precio Base: ${self._precio_base}"

class Sala(Servicio):
    def __init__(self, nombre, precio_base, horas):
        super().__init__(nombre, precio_base)
        self.horas = horas

    def calcular_precio(self):
        return self._precio_base * self.horas

class Equipo(Servicio):
    def __init__(self, nombre, precio_base, dias):
        super().__init__(nombre, precio_base)
        self.dias = dias

    def calcular_precio(self):
        # El alquiler de equipos tiene un descuento del 10% si es por más de 5 días
        total = self._precio_base * self.dias
        return total * 0.9 if self.dias > 5 else total

class Asesoria(Servicio):
    def __init__(self, nombre, precio_base, nivel_complejidad):
        super().__init__(nombre, precio_base)
        self.nivel_complejidad = nivel_complejidad 

    def calcular_precio(self):
        return self._precio_base * self.nivel_complejidad
    
class Cliente:
    def __init__(self, id_cliente, nombre, email):
        self.__id_cliente = id_cliente  # Atributo privado
        self.__nombre = nombre
        self.__email = email

    @property
    def nombre(self):
        return self.__nombre

    def __str__(self):
        return f"Cliente: {self.__nombre} (ID: {self.__id_cliente})"
    
class Reserva:
    def __init__(self, cliente, servicio):
        self.__id_reserva = id(self) # Genera un ID único basado en la dirección de memoria
        self.__cliente = cliente
        self.__servicio = servicio
        self.__fecha = datetime.now()

    def mostrar_detalle(self):
        return (f"Reserva ID: {self.__id_reserva} | Fecha: {self.__fecha.strftime('%Y-%m-%d %H:%M')}\n"
                f"  {self.__cliente}\n"
                f"  {self.__servicio} | Total a pagar: ${self.__servicio.calcular_precio():.2f}")
        
class SoftwareFJ:
    def __init__(self):
        self.__reservas = []
        self.__clientes = {}

    def registrar_cliente(self, cliente):
        self.__clientes[cliente.nombre] = cliente
        print(f"✅ Cliente {cliente.nombre} registrado con éxito.")

    def crear_reserva(self, cliente, servicio):
        try:
            # Creamos la reserva vinculando los objetos
            nueva_reserva = Reserva(cliente, servicio)
            self.__reservas.append(nueva_reserva)
            print("🚀 Reserva procesada correctamente.")
            return nueva_reserva
        except Exception as e:
            print(f"❌ Error al crear la reserva: {e}")

    def listar_reservas(self):
        print("\n--- 📝 LISTADO DE RESERVAS ACTUALES ---")
        if not self.__reservas:
            print("No hay reservas registradas.")
        for r in self.__reservas:
            print(r.mostrar_detalle())
            print("-" * 40)
            
