import json
from pathlib import Path
from django.shortcuts import render, redirect

BASE_DIR = Path(__file__).resolve().parent.parent
SERVICIOS_PATH = BASE_DIR / 'servicios.json'
DATOS_PATH = BASE_DIR / 'datos.json'


def cargar_servicios():
    with open(SERVICIOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def guardar_registro(registro):
    try:
        with open(DATOS_PATH, 'r', encoding='utf-8') as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = []
    registros.append(registro)
    with open(DATOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(registros, f, indent=2, ensure_ascii=False)


def evaluar_decision(servicios, ofrecido, horas_ofrecidas, solicitado, horas_solicitadas):
    # validaciones
    if horas_ofrecidas < 0 or horas_solicitadas < 0:
        return None, 'Error: horas inválidas'
    if ofrecido not in servicios or solicitado not in servicios:
        return None, 'Error: servicio no encontrado'

    valor_ofrecido = horas_ofrecidas * servicios[ofrecido]
    valor_solicitado = horas_solicitadas * servicios[solicitado]
    diferencia = valor_ofrecido - valor_solicitado

    if diferencia == 0:
        estado = 'Intercambio Perfecto'
        mensaje = 'Valores equivalentes. Intercambio 100% equitativo.'
    elif diferencia > 0:
        estado = 'Intercambio Favorable para el Receptor'
        mensaje = 'Usted ofrece más valor del que solicita.'
    elif diferencia < 0 and diferencia >= -(valor_solicitado * 0.20):
        estado = 'Requiere Ajuste Menor'
        mensaje = 'La diferencia negativa no supera el 20%: considere agregar horas.'
    else:
        estado = 'Intercambio Desproporcionado (Rechazado)'
        mensaje = 'La diferencia supera el 20%: replantee la oferta.'

    resultado = {
        'servicio_ofrecido': ofrecido,
        'horas_ofrecidas': horas_ofrecidas,
        'servicio_solicitado': solicitado,
        'horas_solicitadas': horas_solicitadas,
        'valor_ofrecido': valor_ofrecido,
        'valor_solicitado': valor_solicitado,
        'diferencia': diferencia,
        'estado': estado,
        'mensaje': mensaje,
    }
    return resultado, None


def simulador(request):
    servicios = cargar_servicios()
    resultado = None
    error = None

    if request.method == 'POST':
        ofrecido = request.POST.get('servicio_ofrecido')
        solicitado = request.POST.get('servicio_solicitado')
        try:
            horas_ofrecidas = int(request.POST.get('horas_ofrecidas', '0'))
            horas_solicitadas = int(request.POST.get('horas_solicitadas', '0'))
        except ValueError:
            error = 'Horas deben ser enteros'
            return render(request, 'simulador.html', {'servicios': servicios, 'error': error})

        resultado, error = evaluar_decision(servicios, ofrecido, horas_ofrecidas, solicitado, horas_solicitadas)
        if resultado:
            registro = {
                'servicio_ofrecido': ofrecido,
                'horas_ofrecidas': horas_ofrecidas,
                'servicio_solicitado': solicitado,
                'horas_solicitadas': horas_solicitadas,
                'valor_ofrecido': resultado['valor_ofrecido'],
                'valor_solicitado': resultado['valor_solicitado'],
                'diferencia': resultado['diferencia'],
                'estado': resultado['estado'],
            }
            guardar_registro(registro)
            # redirigir por PRG para evitar repost
            return render(request, 'simulador.html', {'servicios': servicios, 'resultado': resultado})

    return render(request, 'simulador.html', {'servicios': servicios})
