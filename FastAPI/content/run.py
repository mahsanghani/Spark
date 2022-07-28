import requests
import time

ner_text = """
A 28-year-old female with a history of gestational diabetes mellitus diagnosed eight years prior to presentation and subsequent type two diabetes mellitus ( T2DM ), one prior episode of HTG-induced pancreatitis three years prior to presentation , associated with an acute hepatitis , and obesity with a body mass index ( BMI ) of 33.5 kg/m2 , presented with a one-week history of polyuria , polydipsia , poor appetite , and vomiting. The patient was prescribed 1 capsule of Advil 10 mg for 5 days and magnesium hydroxide 100mg/1ml suspension PO. 
He was seen by the endocrinology service and she was discharged on 40 units of insulin glargine at night , 12 units of insulin lispro with meals , and metformin 1000 mg two times a day.
"""
# Change this line to execute any of the two pipelines
modelname = 'clinical_deidentification'
# modelname = 'ner_profiling_clinical'

query = f"?modelname={modelname}&text={ner_text}"
url = f"http://localhost:8515/benchmark/pipeline{query}"
print(requests.get(url))

def explode_annotate(ann_result):
   '''
   Function to convert result object to json
   input: raw result
   output: processed result dictionary
   '''
   result = {}
   for column, ann in ann_result[0].items():
       result[column] = []
       for lines in ann:
           content = {
              "result": lines.result,
              "begin": lines.begin,
              "end": lines.end,
              "metadata": dict(lines.metadata),
           }
           result[column].append(content)
   return result