#!/usr/bin/env python3
"""Cuatro factores y avanzadas de equipo a partir de los totales del primer tiempo.

Las fórmulas están verificadas contra el informe de la fecha 5 (ICCAN 32 -
Ambato Soldiers 31): reproducen los diez valores de la tabla de avanzadas.

    python3 calcular.py            # corre la verificación contra la fecha 5
"""


def avanzadas(equipo, rival):
    """equipo y rival: dicts con pts, dos (m,a), tres (m,a), tl (m,a), ro, rd, per."""
    tcc = equipo["dos"][0] + equipo["tres"][0]          # tiros de campo convertidos
    tci = equipo["dos"][1] + equipo["tres"][1]          # tiros de campo intentados
    tli = equipo["tl"][1]

    # posesiones: la estimación clásica, con 0.44 por viaje a la línea
    pos = tci - equipo["ro"] + equipo["per"] + 0.44 * tli
    pos_rival = (rival["dos"][1] + rival["tres"][1]) - rival["ro"] + rival["per"] + 0.44 * rival["tl"][1]

    return {
        "efg": (tcc + 0.5 * equipo["tres"][0]) / tci * 100 if tci else 0,
        "ts": equipo["pts"] / (2 * (tci + 0.44 * tli)) * 100 if tci or tli else 0,
        "tov": equipo["per"] / pos * 100 if pos else 0,
        # el rebote ofensivo se mide contra el defensivo que le queda al rival
        "orb": equipo["ro"] / (equipo["ro"] + rival["rd"]) * 100 if (equipo["ro"] + rival["rd"]) else 0,
        "ftr": tli / tci * 100 if tci else 0,
        "ortg": equipo["pts"] / pos * 100 if pos else 0,
        "drtg": rival["pts"] / pos_rival * 100 if pos_rival else 0,
    }


def redondear(d):
    return {k: round(v) for k, v in d.items()}


if __name__ == "__main__":
    # fecha 5 · ICCAN vs Ambato Soldiers, primer tiempo
    iccan = {"pts": 32, "dos": (9, 18), "tres": (4, 16), "tl": (2, 4), "ro": 9, "rd": 15, "per": 7}
    ambato = {"pts": 31, "dos": (9, 19), "tres": (2, 10), "tl": (7, 9), "ro": 4, "rd": 13, "per": 6}

    esperado = {
        "ICCAN":           {"efg": 44, "ts": 45, "tov": 21, "orb": 41, "ftr": 12, "ortg": 95, "drtg": 89},
        "Ambato Soldiers": {"efg": 41, "ts": 47, "tov": 17, "orb": 21, "ftr": 31, "ortg": 89, "drtg": 95},
    }

    todo_ok = True
    for nombre, (eq, riv) in {"ICCAN": (iccan, ambato), "Ambato Soldiers": (ambato, iccan)}.items():
        obtenido = redondear(avanzadas(eq, riv))
        for clave, valor in esperado[nombre].items():
            marca = "ok" if obtenido[clave] == valor else "NO COINCIDE"
            if obtenido[clave] != valor:
                todo_ok = False
            print(f"{nombre:16} {clave:5} calculado {obtenido[clave]:3}  informe {valor:3}  {marca}")

    print("\nTodas las fórmulas coinciden con el informe de la fecha 5."
          if todo_ok else "\nHay valores que no coinciden: revisar antes de usar.")
