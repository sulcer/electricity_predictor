import os
import great_expectations as ge
import pandas as pd
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from src.logger_config import logger


def main():
    context = ge.get_context()

    for file in os.listdir("data/processed"):
        if not file.startswith("reference_") and file.endswith(".csv"):
            expectation_subject = file.replace(".csv", "")

            logger.info(f"Running GX checkpoint validation for {expectation_subject}")

            result: CheckpointResult = context.run_checkpoint(checkpoint_name=f"{expectation_subject}_checkpoint")

            if not result["success"]:
                logger.error(f"GX checkpoint validation for {expectation_subject} failed!")
                # raise ValueError("Checkpoint failed")
            elif result["success"]:
                logger.info(f"GX checkpoint validation for {expectation_subject} successful!")

            current_data = pd.read_csv(f"data/processed/{file}")
            reference_data_path = f"data/processed/reference_{file}"
            current_data.to_csv(reference_data_path, index=False)


if __name__ == "__main__":
    main()
