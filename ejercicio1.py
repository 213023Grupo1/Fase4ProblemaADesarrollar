from abc import ABC, abstractmethod

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