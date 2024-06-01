import os
import pandas as pd
from evidently.test_preset import DataStabilityTestPreset
from evidently.test_suite import TestSuite
from src.logger_config import logger

if __name__ == "__main__":
    tests = TestSuite(tests=[
        DataStabilityTestPreset()
    ])

    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            tests_subject = file.replace(".csv", "")

            logger.info(f"Running Stability test for {tests_subject}")

            current_data = pd.read_csv(f"data/processed/{file}")
            reference_data = pd.read_csv(f"data/processed/reference_{file}")

            tests.run(reference_data=current_data, current_data=reference_data)

            tests.save_html(f"reports/sites/{tests_subject}_stability_tests.html")
