from utils import tokenizar, expandir_plus, expandir_question, insertar_concatenacion
from shunting_yard import shunting_yard
from balanceador import balanceada
from arbol_sintactico import construir_arbol_sintactico
from visualizador import dibujar_arbol, dibujar_afn
from afn import construir_afn_thompson

def procesar(expresion, cadena="", numero=None, mostrar_arbol=True, mostrar_afn=True):
    print("=" * 80)
    print("Expresión regular:")
    print(expresion)
    print("Cadena a reconocer:")
    print(repr(cadena))

    if not balanceada(expresion):
        print("\nERROR: expresión no balanceada.")
        return None

    try:
        tokens = tokenizar(expresion)
        print("\nTokens:")
        print(tokens)

        tokens = expandir_plus(tokens)
        print("\nDespués de expandir +:")
        print(tokens)

        tokens = expandir_question(tokens)
        print("\nDespués de expandir ?:")
        print(tokens)

        tokens = insertar_concatenacion(tokens)
        print("\nDespués de insertar concatenación:")
        print(tokens)

        postfix = shunting_yard(tokens)
        print("\nPostfix:")
        print(" ".join(postfix))

        arbol = construir_arbol_sintactico(postfix)
        print("\nÁrbol sintáctico:")
        print("Preorden:", " -> ".join(arbol.preorden()))
        print("Altura:", arbol.altura())

        if mostrar_arbol:
            dibujar_arbol(
                arbol,
                expresion,
                numero=numero,
                mostrar=True,
                guardar=True
            )

        afn = construir_afn_thompson(arbol)

        print("\nAFN de Thompson:")
        print(f"Estado inicial: q{afn.inicial.id}")
        print(f"Estado de aceptación: q{afn.aceptacion.id}")
        print(f"Cantidad de estados: {len(afn.estados)}")

        if mostrar_afn:
            dibujar_afn(
                afn,
                expresion,
                numero=numero,
                mostrar=True,
                guardar=True
            )

        aceptada, traza = afn.simular(cadena)
        print("\nSimulación del AFN:")
        print(f"ε-cierre inicial: {formatear_estados(traza[0][1])}")

        for simbolo, estados in traza[1:]:
            print(f"Con '{simbolo}' -> {formatear_estados(estados)}")

        resultado = "sí" if aceptada else "no"
        print(f"\n¿w ∈ L(r)? {resultado}")

        return {
            "arbol": arbol,
            "afn": afn,
            "aceptada": aceptada,
            "traza": traza
        }

    except ValueError as e:
        print("\nERROR:", e)
        return None

def formatear_estados(estados):
    if not estados:
        return "∅"
    return "{" + ", ".join(f"q{estado}" for estado in estados) + "}"
