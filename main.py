from sensor.logger import logging
from sensor.exception import SensorException
from sensor.utils import  get_collections_as_dataframe
import sys,os
from sensor.entity import config_entity
from sensor.components.dataingestion import DataIngestion
from sensor.components.datavalidation import DataValidation
from sensor.components.datatransformation import DataTransformation
from sensor.components.modeltrainer import ModelTrainer
from sensor.components.modelevaluation import ModelEvaluation
from sensor.components.modelpusher import ModelPusher
from sensor.predictor import ModelResolver 

'''def test_logger_and_exception():
    try:
        result = 3/10
        print(result)
    except Exception as e:
        raise SensorException(e,sys)'''
# if __name__ == "__main__":
#     obj = ModelResolver()
#     path = obj.get_latest_dir_path()
#     print(path)

if __name__=="__main__":
    try:
        #get_collections_as_dataframe(database_name="aps",collection_name="sensor")
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        #data ingestion
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config) 
        print(data_ingestion_config.to_dict())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        #data validation
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config = training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                        data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()

        #data transformation
        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
                                                  data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        #model trainer
        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config = training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                     data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

        #model evaluation
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config = training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config = model_eval_config,
                                    data_ingestion_artifact=data_ingestion_artifact,
                                    data_transformation_artifact=data_transformation_artifact,
                                    model_trainer_artifact=model_trainer_artifact)
        model_evaluation_artifact = model_eval.initiate_model_evaluation()
        
        #model pusher
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config = training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config = model_pusher_config,
                                   data_transformation_artifact = data_transformation_artifact,
                                   model_trainer_artifact = model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
    except Exception as e:
        print(e)
