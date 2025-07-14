import pandas as pd

def save_to_csv(data: list[dict], filename: str):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
 
