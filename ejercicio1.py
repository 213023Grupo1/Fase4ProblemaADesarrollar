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
        
    @property
    def nivel_complejidad(self):
        return self._nivel_complejidad
    
    @nivel_complejidad.setter
    def nivel_complejidad(self, valor):
        if not (1 <= valor <= 3):
            raise ServicioInvalidadoError(f"Nivel {valor} no valido. Debe ser entre 1 y 3.")
        self._nivel_complejidad = valor

    def calcular_precio(self):
        return self._precio_base * self._nivel_complejidad
    
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

    def crear_reserva(self, id_cliente, servicio):
        try:
            # validacion de existencia de cliente
            if id_cliente not in self.__clientes:
                raise ClienteNoEncontradoError(f"el cliente con ID {id_cliente} no existe.")
            
            if servicio.calcular_precio() <= 0:
                raise ReservaError(f"El costo de la reserva no puede seer cero")
                
            nueva_reserva = Reserva(self.__clientes[id_cliente], servicio)
            self.__reservas.append(nueva_reserva)
            print(f"🚀 Reserva para {servicio._nombre} creada con exito.")
        
        except SoftwareFJError as e:
            print(f"❌ Error de negocio: {e}")
            
        except Exception as e:
            print(f"❌ Error critico del sistema: {e}")
            
        finally:
            print("✔ operacion de reserva finalizada.")
            

    def listar_reservas(self):
        print("\n--- 📝 LISTADO DE RESERVAS ACTUALES ---")
        if not self.__reservas:
            print("No hay reservas registradas.")
        for r in self.__reservas:
            print(r.mostrar_detalle())
            print("-" * 40)
            
# 1. Instanciar el sistema central
sistema = SoftwareFJ()

# 2. Crear clientes
juan = Cliente("001", "Juan Perez", "juan@mail.com")
sistema.registrar_cliente(juan)

# 3. Crear servicios (Polimorfismo en acción)
sala_reunion = Sala("Sala de Conferencias A", precio_base=50, horas=4)
equipo_laptop = Equipo("MacBook Pro Alquiler", precio_base=30, dias=6) # Aplica descuento > 5 días

# 4. Gestionar reservas
sistema.crear_reserva(juan, sala_reunion)
sistema.crear_reserva(juan, equipo_laptop)

# 5. Ver resultados
sistema.listar_reservas()

# clase base para excepciones
class SoftwareFJError(Exception):
    pass

# se lanza cuando los parametros de un servicio son ilogicos
class ServicioInvalidadoError(SoftwareFJError):
    pass 

# se lanza cuando se va a operar con un cliente no existente
class ClienteNoEncontradoError(SoftwareFJError):
    pass

# errores generales en el proceso de reserva
class ReservaError(SoftwareFJError):
    pass

