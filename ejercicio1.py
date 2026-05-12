from abc import ABC, abstractmethod

class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self._nombre = nombre
        self._precio_base = precio_base

    @abstractmethod
    def calcular_precio(self, impuesto=0, descuento=0):
        pass
    
    def __str__(self):
            return f"Servicio: {self._nombre} | Precio Base: ${self._precio_base}"

class Sala(Servicio):
    def __init__(self, nombre, precio_base, horas):
        super().__init__(nombre, precio_base)
        self.horas = horas

    def calcular_precio(self, impuesto=0, descuento=0):
        total = self._precio_base * self.horas
        
        total += total * impuesto
        total -= total * descuento
        
        return total

class Equipo(Servicio):
    def __init__(self, nombre, precio_base, dias):
        super().__init__(nombre, precio_base)
        self.dias = dias

    def calcular_precio(self, impuesto=0, descuento=0):
        # El alquiler de equipos tiene un descuento del 10% si es por más de 5 días
        total = self._precio_base * self.dias
        if self.dias > 5:
            total *= 0.9
            
        total += total * impuesto
        total -= total * descuento
        
        return total

class Asesoria(Servicio):
    def __init__(self, nombre, precio_base, nivel_complejidad):
        super().__init__(nombre, precio_base)
        self.nivel_complejidad = nivel_complejidad 

    def calcular_precio(self, impuesto=0, descuento=0):
        total = self._precio_base * self.nivel_complejidad
        
        total += total * impuesto
        total -= total * descuento
        
        return total