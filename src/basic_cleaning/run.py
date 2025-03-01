#!/usr/bin/env python
"""
Downloads the raw dataset from W&B;
apply some basic data cleaning, and finally exporting the result to a new artifact.
"""
import os
import argparse
import logging

import pandas as pd

import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info('*** fetching the artifact...')
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info('*** perform basic cleaning on dataset...')
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx]

    # convert `last_review` to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # remove samples outside nyc
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx]

    logger.info('*** saving the clean file & logging the artifact...')
    output_file_path = 'clean_sample.csv'
    df.to_csv(output_file_path, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file('clean_sample.csv')
    run.log_artifact(artifact)

    # Remove the local file
    os.remove(output_file_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic data cleaning")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help='input artifact path',
        required=True,
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help='output artifact path',
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help='output type',
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help='basic description of output',
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help='price lower bound',
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help='price upper bound',
        required=True
    )


    args = parser.parse_args()

    go(args)
