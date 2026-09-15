import pandas, sys

unidade = sys.argv[1]

pandas.read_csv(f"{unidade}.csv").drop(columns=["NPU", "duration"]).to_csv(f"{unidade}.csv", index=False)