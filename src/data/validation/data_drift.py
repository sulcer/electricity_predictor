import os
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from src.logger_config import logger

if __name__ == "__main__":
    report = Report(metrics=[DataDriftPreset()])

    for file in os.listdir("data/processed"):
        if file.startswith("reference_") and file.endswith(".csv"):
            file = file.replace("reference_", "")
            drift_subject = file.replace(".csv", "")

            logger.info(f"Running data drift validation for {drift_subject}")

            current = pd.read_csv(f"data/processed/{file}")
            reference = pd.read_csv(f"data/processed/reference_{file}")

            report.run(reference_data=reference, current_data=current)

            report.save_html(f'reports/sites/{drift_subject}_drift.html')
