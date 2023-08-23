def convert_wind_speed(wind_speed_mps, target_unit):
    mps_to_kph = 3.6
    mps_to_mph = 2.23694
    mps_to_knots = 1.94384

    wind_speed_kph = wind_speed_mps * mps_to_kph
    wind_speed_mph = wind_speed_mps * mps_to_mph
    wind_speed_knots = wind_speed_mps * mps_to_knots

    beaufort_scale = [
        (0.0, "Windstille: 0"),
        (0.3, "Windstille: 0"),
        (1.6, "Flaues Lüftchen: 1"),
        (3.4, "Leichte Brise: 2"),
        (5.5, "Schwache Brise: 3"),
        (8.0, "Mäßige Brise: 4"),
        (10.8, "Frische Brise: 5"),
        (13.9, "Starker Wind: 6"),
        (17.2, "Steifer Wind: 7"),
        (20.8, "Stürmischer Wind: 8"),
        (24.5, "Sturm: 9"),
        (28.5, "Schwerer Sturm: 10"),
        (32.7, "Orkanartiger Sturm: 11")
    ]

    beaufort_wind_speed = ""
    for cutoff, description in beaufort_scale:
        if wind_speed_mps < cutoff:
            beaufort_wind_speed = description
            break
    else:
        beaufort_wind_speed = "Orkan: 12"

    units = {
        "m/s": wind_speed_mps,
        "km/h": wind_speed_kph,
        "mph": wind_speed_mph,
        "knots": wind_speed_knots,
        "Bft": beaufort_wind_speed
    }

    return units[target_unit]

# Beispielgeschwindigkeit in m/s
wind_speed_mps = 40.0

# Gewünschte Einheit auswählen
target_unit = "Bft"

# Umrechnung aufrufen
converted_value = convert_wind_speed(wind_speed_mps, target_unit)

# Ergebnis ausgeben
print(f"{converted_value} {target_unit}")
