import os
from pathlib import Path

# import some usable methods
from blocks.core.generate.save import SaveNode
from blocks.core.postgenerate.evaluation import (EvaluatedObject,
                                                 EvaluationUtility)
from blocks.core.pregenerate.statistics import (filter_grouped_by,
                                                group_by_class, subject_counts)

__all__ = [
    "DATA", "OPTIONS", "BASE_DIR", "STATIC_ROOT"
    "SaveNode",
    "EvaluatedObject","EvaluationUtility",
    "filter_grouped_by", "group_by_class",
    "subject_counts"
]

from blocks.util.csv import read_csv
from blocks.util.imports import import_from_settings

from .pregenerate.clean import clean_options, populate_with_id

BASE_DIR = import_from_settings(
    "BASE_DIR", 
    default=Path(__file__).resolve().parent.parent
    )

STATIC_ROOT = import_from_settings(
    "STATIC_ROOT",
    default=os.path.join(BASE_DIR, "static")
)

# get data and options from a static csv file. This is only used for debug
# and so do not read during production

DATA = None
OPTIONS = None

if import_from_settings("data_and_options_use_static", default=False):
    # only read from static during testing the generator module
    default_max_opts = import_from_settings("default_max_options", default=4)
    cleaned = [
        clean_options(opts, default_max_opts) for opts in read_csv(os.path.join(STATIC_ROOT, "data.csv"))
        ]
    DATA = populate_with_id(cleaned)
    OPTIONS = [subj[1] for subj in read_csv(os.path.join(STATIC_ROOT, "options.csv"))]

