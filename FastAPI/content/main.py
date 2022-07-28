import uvicorn, json, os
from fastapi import FastAPI
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *
from sparknlp.base import *
import sparknlp, sparknlp_jsl
from sparknlp.pretrained import PretrainedPipeline
app = FastAPI()
pipelines = {}