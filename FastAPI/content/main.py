import uvicorn, json, os
from fastapi import FastAPI
from sparknlp.annotator import *
from sparknlp_jsl.annotator import *
from sparknlp.base import *
import sparknlp, sparknlp_jsl
from sparknlp.pretrained import PretrainedPipeline
app = FastAPI()
pipelines = {}

@app.get("/benchmark/pipeline")
async def get_one_sequential_pipeline_result(modelname, text=''):
    return pipelines[modelname].annotate(text)


@app.on_event("startup")
async def startup_event():
    with open('/content/sparknlp_keys.json', 'r') as f:
        license_keys = json.load(f)


spark = sparknlp_jsl.start(secret=license_keys['SECRET'])

pipelines['ner_profiling_clinical'] = PretrainedPipeline('ner_profiling_clinical', 'en', 'clinical/models')

pipelines['clinical_deidentification'] = PretrainedPipeline("clinical_deidentification", "en", "clinical/models")

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8515)