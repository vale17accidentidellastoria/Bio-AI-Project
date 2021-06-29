import statistics as st

TRANSPORT_MODES = {
    "truck": "road_transport",
    "sea_ship": "maritime_transport",
    "train": "railway_transport",
    "airplane": "air_transport"
}

TRANSPORT_MODE_DATA = {
    "road_transport": {
        "costs_tonkm": 0.366,
        "energy_consumption": 1.21
    },
    "maritime_transport": {
        "costs_tonkm": 0.0032,
        "energy_consumption": 0.09
    },
    "railway_transport": {
        "costs_tonkm": 0.012,
        "energy_consumption": 0.33
    },
    "air_transport": {
        "costs_tonkm": 0.18,
        "energy_consumption": 9.77
    }
}

def co2_score(val):
    score = 0
    if val >= 1:
        score = 0
    elif 0.1 <= val < 1:
        score = 3.5
    elif 0.01 <= val < 0.1:
        score = 5.0
    elif 0.001 <= val < 0.01:
        score = 7.0
    elif 0.0001 <= val < 0.001:
        score = 8.5
    elif 0 <= val < 0.0001:
        score = 10.0
    return score

def transport_penalty(val):
    penalty = 0
    if val >= 0.1:
        penalty = 1.0
    elif 0.01 <= val < 0.1:
        penalty = 0.5
    elif 0 <= val < 0.01:
        penalty = 0.1
    return penalty

def compute_transport_sustainability_index(G, shortest_path, edge_attrs):
    co2_wtw_values = []
    distance_values = []
    lf_values = []
    cost_values = []
    energy_consumption_values = []

    for country, next_country in zip(shortest_path, shortest_path[1:]):
        for attr in edge_attrs:
            value = G[country][next_country][attr]
            if attr == "co2_wtw":
                co2_wtw_values.append(value)
            elif attr == "distance_wtw":
                distance_values.append(value)
            elif attr == "load_factor":
                lf_values.append(value)
            if attr == "transport_mode":
                cost_values.append(TRANSPORT_MODE_DATA[TRANSPORT_MODES[value]]["costs_tonkm"])
                energy_consumption_values.append(TRANSPORT_MODE_DATA[TRANSPORT_MODES[value]]["energy_consumption"])
    
    score = co2_score(sum(co2_wtw_values)/sum(distance_values))
    penalty = transport_penalty(sum(cost_values)/sum(energy_consumption_values))
    avg_lf = st.mean(lf_values)/100

    index = round(avg_lf * (score - penalty), 2)

    return index
