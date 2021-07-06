from numpy import disp
import pandas as pd
import dataframe_image as dfi
from PIL import Image

countries = ["India", "China", "Italy", "USA", "Bangladesh", "Peru", "Egypt", "Turkey", "Vietnam", "Uzbekistan"]

fertilizer = {"india" : 990 ,
"egypt" : 690,
"turkey" : 730,
"bangladesh":  825,
"vietnam" : 884,
"italy" : 895 - 200 ,
"china" : 1000,
"peru" : 980,
"uzbekistan" : 1125,
"usa" : 1127  - 400}

water = {"india" : 38 ,
"egypt" : 35,
"turkey" : 40,
"bangladesh":  25,
"vietnam" : 28,
"italy" :  50,
"china" : 25,
"peru" : 39,
"uzbekistan" : 21,
"usa" : 60    
}

def multiplier(f): 
    if f >= 547 and f <= 662:
        mult = 1.88
    if f >= 663 and f <= 778:
        mult = 2.086        
    if f >= 779 and f <= 894:   
        mult = 2.282             
    if f >= 895 and f <= 1010:
        mult = 2.478         
    if f >= 1011 and f <= 1126:
        mult = 2.674    
    if f >= 1127: 
        mult = 2.87 
    return mult


def create_dataframe(countries, fertilizer, water):
    columns = ["Country","Fertilizer", "Multiplier fert","Fertilizer waste index",
                         "Water efficiency", "Water efficiency index", "Final Index"]
    df = pd.DataFrame(columns=columns)
    df["Country"] = countries
    for idx, el in df.iterrows():
        f = fertilizer[el.Country.lower()]
        df.loc[df.Country==el.Country, "Fertilizer"] = f
        w = water[el.Country.lower()]
        df.loc[df.Country==el.Country, "Water efficiency"] = w 
        df.loc[df.Country==el.Country, "Multiplier fert"] = multiplier(f)
    df["Fertilizer waste index"] = 1 - (((df["Fertilizer"]* df["Multiplier fert"])-1028.36)/2206.13)
    df["Water efficiency index"] = 1 - (((100-df["Water efficiency"])-2)/78)
    df["Final Index"] = (6*df["Fertilizer waste index"]) + (4 * df["Water efficiency index"])
    df.to_csv("data/production_index.csv")
    return df 


def compute_production_sustainability_index():
    df = create_dataframe(countries, fertilizer, water)
    idx= df["Final Index"].values
    obj_zip = zip(countries, idx)    
    index_prod = dict(obj_zip)
    final = df[["Country", "Fertilizer waste index", "Water efficiency index", "Final Index"]].copy()
    final = final.sort_values(by="Final Index").reset_index().drop(columns="index")
    final.style.background_gradient(cmap="RdYlGn", subset="Final Index", vmin=0, vmax=10).export_png('data/final.png')
    return index_prod, df 




