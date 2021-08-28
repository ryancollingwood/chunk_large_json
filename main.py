import argparse
import uuid
from math import ceil
import pathlib
from datetime import datetime
from multiprocessing import Pool
from functools import partial
import pandas as pd
from tqdm import tqdm


def save_chunk(df_chunk, output_dir):
    outfile = f"{output_dir}{uuid.uuid4()}.json"
    # TODO could make the orientation a param settable
    # through arguments
    df_chunk.to_json(outfile, orient="records")


def check_args(args):

    # check input_file exists
    path_input_file = pathlib.Path(args.input_file)
    if not path_input_file.exists():
        raise ValueError(
            f"{args.input_file} doesn't exist, recheck considering relative paths and such")

    # esnure output_dir ends with a "/"
    if args.output_dir[-1] != "/":
        args.output_dir = f"{args.output_dir}/"

    # check that the output dir doesn't already exist
    # could improve this to check that it's an empty dir
    path_output_dir = pathlib.Path(args.output_dir)
    if path_output_dir.exists():
        raise ValueError(
            f"{args.output_dir} already exists - please specify another output directory or delete it")
    else:
        # create the output folder
        path_output_dir.mkdir(parents=True)

    # can't chunk more rows than we read in
    if args.nrows:
        if args.nrows <= args.chunksize:
            raise ValueError(
                f"Number of rows to be loaded ({args.nrows}) is smaller than chunksize ({args.chunksize}) - load more rows or reduce chunksize.")


def execute(input_file, output_dir, chunksize, nrows=None):

    num_tasks = None
    if nrows:
        num_tasks = ceil(nrows / chunksize)
    else:
        # determining the number of lines in a large file (ergo tasks)
        # takes a long time not worth the trouble
        pass

    chunked_df = pd.read_json(input_file, chunksize=chunksize,
                              lines=True, nrows=nrows)

    with Pool() as p:
        start = datetime.now()

        # used https://clay-atlas.com/us/blog/2021/08/02/python-en-use-multi-processing-pool-progress-bar/
        # as reference for displaying progress bar
        for _ in tqdm(
            p.imap_unordered(
                partial(save_chunk, output_dir=output_dir), chunked_df, chunksize=1),
            total=num_tasks
        ):
            pass

        p.close()
        p.join()

        print("duration in seconds", (datetime.now()-start).total_seconds())


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(prog="Large JSON Chunker",
                                         description="Write out a large JSON file into multiple smaller files")

    arg_parser.add_argument("-input_file",
                            help="path to large JSON file")

    arg_parser.add_argument("-output_dir",
                            help="Output directory where we'll write out the data - must NOT already exist e.g. output/")

    arg_parser.add_argument("-nrows",
                            help="Number of lines to read from large JSON file. If not specified all lines are used.",
                            nargs="?",
                            default=None,
                            type=int
                            )

    arg_parser.add_argument("-chunksize",
                            help="Process the large JSON file as separate chunks of this size",
                            nargs="?",
                            default=10_000,
                            type=int
                            )

    args = arg_parser.parse_args()

    check_args(args)

    execute(args.input_file, args.output_dir, args.chunksize, args.nrows)
