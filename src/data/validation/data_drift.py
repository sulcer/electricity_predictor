import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

if __name__ == "__main__":
    report = Report(metrics=[DataDriftPreset()])

    current = pd.read_csv("data/processed/price_data.csv")
    reference = pd.read_csv("data/processed/reference_price_data.csv")

    report.run(reference_data=reference, current_data=current)

    report.save_html("reports/sites/price_data_drift.html")
