import os
from openai import OpenAI
from typing import List, Dict, Optional
import numpy as np
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer
from collections import Counter

def fuzzy_match(
    str1: str,
    str2: str,
):
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user_prompt = (
        "You are trying to figure out whether two steps in two different action traces are the same."
    )
    user_prompt += "The first step is" + str1
    user_prompt += " The second step is" + str2
    user_prompt += """ Your response should be in the following format: YES or NO. 

Correctness: [True/False]
Reason: [Reason for the correctness/incorrectness of the agent's output]

Respond True if the agent's output is correct and contains all the relevant information as well."""
    messages = [
        {"role": "system", "content": "You are verifying the correctness of an agent's output. Respond appropriately based on the correctness of the agent's output."},
        {"role": "user", "content": user_prompt},
    ]
    response = openai.chat.completions.create(
        model="gpt-4", messages=messages, max_tokens=400, temperature=0.0, stream=False
    )
    print (response.choices[0].message.content)
    return "true" in response.choices[0].message.content.lower().strip(), response.choices[0].message.content
