# Copyright opensearch-ml-quickstart contributors
# SPDX-License-Identifier: Apache-2.0

import logging
from unittest.mock import patch
from opensearch_py_ml.ml_commons import MLCommonClient

from client import get_client, get_client_configs, OsMlClientWrapper
from ml_models import get_remote_model_configs, get_aos_connector_helper
from ml_models import AosBedrockMlConnector, AosSagemakerMlConnector, RemoteMlModel


def test():
    logging.info("Testing aos opensearch client...")
    os_client = get_client("aos")
    client = OsMlClientWrapper(os_client)
    ml_commons_client = MLCommonClient(os_client=os_client)

    aos_connector_helper = get_aos_connector_helper(get_client_configs("aos"))
    aos_bedrock_configs = get_remote_model_configs(
        host_type="aos", model_type="bedrock"
    )
    aos_sagemaker_configs = get_remote_model_configs(
        host_type="aos", model_type="sagemaker"
    )
    aos_bedrock_ml_connector = AosBedrockMlConnector(
        os_client=os_client,
        connector_configs=aos_bedrock_configs,
        aos_connector_helper=aos_connector_helper
    )
    aos_sagemaker_ml_connector = AosSagemakerMlConnector(
        os_client=os_client,
        connector_configs=aos_sagemaker_configs,
        aos_connector_helper=aos_connector_helper
    )
    aos_bedrock_ml_model = RemoteMlModel(
        os_client, ml_commons_client, model_configs=aos_bedrock_configs, ml_connector=aos_bedrock_ml_connector
    )
    aos_sagemaker_ml_model = RemoteMlModel(
        os_client, ml_commons_client, model_configs=aos_sagemaker_configs, ml_connector=aos_sagemaker_ml_connector
    )

    logging.info(f"Testing bedrock model")
    logging.info("Setting up for kNN")
    client.setup_for_kNN(
        index_name="amazon_pqa",
        index_settings={"settings": {"number_of_shards": 1}},
        pipeline_name="amazon_pqa_pipeline",
        delete_existing=False,
        ml_model=aos_bedrock_ml_model,
    )
    with patch("builtins.input", return_value="y"):
        client.cleanup_kNN(index_name="amazon_pqa", pipeline_name="amazon_pqa_pipeline")

    logging.info(f"Testing sagemaker model")
    logging.info("Setting up for kNN")
    client.setup_for_kNN(
        index_name="amazon_pqa",
        index_settings={"settings": {"number_of_shards": 1}},
        pipeline_name="amazon_pqa_pipeline",
        delete_existing=False,
        ml_model=aos_sagemaker_ml_model,
    )
    with patch("builtins.input", return_value="y"):
        client.cleanup_kNN(index_name="amazon_pqa", pipeline_name="amazon_pqa_pipeline")
