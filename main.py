from src.feature_engineering import build_features_dataframe

if __name__ == "__main__":
    df = build_features_dataframe()
    print(df.head())
