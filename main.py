# ============================================================
# ARCHIVO PRINCIPAL - main.py
# Simulación del sistema Software FJ
# ============================================================

from reserva import Reserva
from cliente_excepciones_logger import (
    Cliente,
    Logger,
    ErrorClienteInvalido
)

from ejercicio1 import Sala, Equipo, Asesoria


def ejecutar_simulacion():
    print("\n=== INICIO DEL SISTEMA ===\n")

    # ===============================
    # CLIENTES
    # ===============================
    print("🔹 Creando clientes...")

    try:
        c1 = Cliente("Ana Pérez", "ana@email.com", "3001234567", 1)
        c2 = Cliente("Luis Gómez", "luis@email.com", "3117654321", 2)
    except ErrorClienteInvalido as e:
        Logger.registrar("ERROR", str(e))

    # Cliente inválido
    try:
        c3 = Cliente("X", "correo_malo", "123", 3)
    except ErrorClienteInvalido as e:
        print("❌ Error controlado:", e)
        Logger.registrar("ERROR", str(e))

    # ===============================
    # SERVICIOS
    # ===============================
    print("\n🔹 Creando servicios...")

    sala = Sala("Sala VIP", 100, 2)
    equipo = Equipo("Proyector", 50, 6)
    asesoria = Asesoria("Consultoría", 200, 3)

    print(f"Sala precio: {sala.calcular_precio()}")
    print(f"Equipo precio: {equipo.calcular_precio()}")
    print(f"Asesoría precio: {asesoria.calcular_precio()}")

    # ===============================
    # SIMULACIÓN DE OPERACIONES
    # ===============================
    print("\n🔹 Simulación de operaciones...")

    operaciones = [
        ("cliente", c1),
        ("cliente", c2),
        ("servicio", sala),
        ("servicio", equipo),
        ("servicio", asesoria),
    ]

    for tipo, obj in operaciones:
        try:
            print(f"✔️ Procesando {tipo}: {obj}")
        except Exception as e:
            Logger.registrar("ERROR", str(e))
    # ===============================
    # RESERVAS
    # ===============================        
    print("\n🔹 Probando reservas...")

    try:
        r1 = Reserva(c1, sala, 2)
        print(r1)

        r1.confirmar()
        print("Estado:", r1.estado)

        r1.completar()
        print("Estado final:", r1.estado)

    except Exception as e:
        print("❌ Error en reserva:", e)

    # Reserva inválida
    try:
        r2 = Reserva(c1, equipo, -5)
    except Exception as e:
        print("❌ Error controlado en reserva:", e)

    print("\n=== FIN DE LA SIMULACIÓN ===")


# Punto de entrada del programa
if __name__ == "__main__":
    ejecutar_simulacion()