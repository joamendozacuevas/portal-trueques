import json
from pathlib import Path
from tabulate import tabulate

BASE_DIR = Path(__file__).resolve().parent
SERVICIOS_PATH = BASE_DIR / "servicios.json"
DATOS_PATH = BASE_DIR / "datos.json"


def cargar_valores():
    with open(SERVICIOS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_registro(registro):
    try:
        with open(DATOS_PATH, "r", encoding="utf-8") as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = []

    registros.append(registro)
    with open(DATOS_PATH, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)


def evaluar(servicio_ofrecido, horas_ofrecidas, servicio_solicitado, horas_solicitadas, valores):
    if horas_ofrecidas < 0 or horas_solicitadas < 0:
        return None, "Error: horas inválidas"

    if servicio_ofrecido not in valores or servicio_solicitado not in valores:
        return None, "Error: servicio no encontrado"

    valor_ofrecido = horas_ofrecidas * valores[servicio_ofrecido]
    valor_solicitado = horas_solicitadas * valores[servicio_solicitado]
    diferencia = valor_ofrecido - valor_solicitado

    if diferencia == 0:
        estado = "Intercambio Perfecto"
        mensaje = "Valores equivalentes. Intercambio 100% equitativo."
    elif diferencia > 0:
        estado = "Intercambio Favorable para el Receptor"
        mensaje = "Usted ofrece más valor del que solicita."
    elif diferencia < 0 and diferencia >= -(valor_solicitado * 0.20):
        estado = "Requiere Ajuste Menor"
        mensaje = "La diferencia negativa no supera el 20%: considere agregar horas."
    else:
        estado = "Intercambio Desproporcionado (Rechazado)"
        mensaje = "La diferencia supera el 20%: replantee la oferta."

    resultado = {
        "servicio_ofrecido": servicio_ofrecido,
        "horas_ofrecidas": horas_ofrecidas,
        "servicio_solicitado": servicio_solicitado,
        "horas_solicitadas": horas_solicitadas,
        "valor_ofrecido": valor_ofrecido,
        "valor_solicitado": valor_solicitado,
        "diferencia": diferencia,
        "estado": estado,
        "mensaje": mensaje,
    }
    return resultado, None


def main():
    valores = cargar_valores()

    print("Simulador de Intercambio (consola)")
    servicio_ofrecido = input("Servicio ofrecido: ").strip()
    try:
        horas_ofrecidas = int(input("Horas ofrecidas: ").strip())
    except ValueError:
        print("Error: horas ofrecidas deben ser un entero")
        return

    servicio_solicitado = input("Servicio solicitado: ").strip()
    try:
        horas_solicitadas = int(input("Horas solicitadas: ").strip())
    except ValueError:
        print("Error: horas solicitadas deben ser un entero")
        return

    resultado, error = evaluar(servicio_ofrecido, horas_ofrecidas, servicio_solicitado, horas_solicitadas, valores)
    if error:
        print(error)
        return

    registro = {
        "servicio_ofrecido": servicio_ofrecido,
        "horas_ofrecidas": horas_ofrecidas,
        "servicio_solicitado": servicio_solicitado,
        "horas_solicitadas": horas_solicitadas,
        "valor_ofrecido": resultado["valor_ofrecido"],
        "valor_solicitado": resultado["valor_solicitado"],
        "diferencia": resultado["diferencia"],
        "estado": resultado["estado"],
    }

    guardar_registro(registro)

    # Mostrar resumen con tabulate
    try:
        with open(DATOS_PATH, "r", encoding="utf-8") as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = [registro]

    print("\nResultado:")
    print(f"Tus {horas_ofrecidas} hrs de {servicio_ofrecido} valen {resultado['valor_ofrecido']} pts.")
    print(f"Estás pidiendo {horas_solicitadas} hrs de {servicio_solicitado} ({resultado['valor_solicitado']} pts).")
    print(f"Estado: {resultado['estado']}")
    print(f"Detalle: {resultado['mensaje']}")

    print("\nRegistros guardados:")
    print(tabulate(registros, headers="keys", showindex=True))


if __name__ == "__main__":
    main()
