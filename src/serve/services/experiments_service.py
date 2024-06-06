import pandas as pd
import dagshub
from dagshub.data_engine.datasources import mlflow
import dagshub.auth as dh_auth
from src.config import settings


class ExperimentService:
    def __init__(self):
        pass

    @staticmethod
    def start_dagshub_conn():
        dh_auth.add_app_token(token=settings.dagshub_user_token)
        dagshub.init(settings.dagshub_repo_name, settings.mlflow_tracking_username, mlflow=True)
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

        if mlflow.active_run():
            mlflow.end_run()

    def get_validate_predictions_experiments(self):
        self.start_dagshub_conn()

        cols = ['start_time', 'end_time', 'metrics.mean_error', 'metrics.mean_squared_error']
        df = pd.DataFrame(columns=cols)

        for model_type in settings.prediction_subjects:
            experiments = mlflow.search_runs(
                search_all_experiments=True,
                filter_string=f"attributes.run_name LIKE 'validate_predictions_{model_type}'",
            )

            experiment_df = pd.DataFrame(experiments)[cols]

            if not experiment_df.empty:
                df = pd.concat([df, experiment_df])

        df = df.dropna()
        data_dict = {col: df[col].tolist() for col in cols}
        return data_dict

    def get_train_model_experiments(self):
        self.start_dagshub_conn()

        cols = ['start_time', 'end_time', 'metrics.EVS_latest', 'metrics.MSE_latest', 'metrics.MAE_latest']
        df = pd.DataFrame(columns=cols)

        for model_type in settings.prediction_subjects:
            experiments = mlflow.search_runs(
                search_all_experiments=True,
                filter_string=f"attributes.run_name LIKE 'train_{model_type}_model'",
            )

            experiment_df = pd.DataFrame(experiments)[cols]

            if not experiment_df.empty:
                df = pd.concat([df, experiment_df])

        df = df.dropna()
        data_dict = {col: df[col].tolist() for col in cols}
        return data_dict
