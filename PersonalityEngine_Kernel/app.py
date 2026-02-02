from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import datetime

from PersonalityEngine_Kernel.engines.inference.inference_engine import run_inference

app = FastAPI(title="PEK Lite", version="0.1-truth-test")


class InferenceRequest(BaseModel):
    responses: list[str]


@app.post("/report")
def report(payload: InferenceRequest):
    if not payload.responses:
        raise HTTPException(status_code=400, detail="No responses provided")

    result = run_inference(payload.responses)

    return JSONResponse({
        "DEPLOYMENT_PROOF": {
            "uuid": str(uuid.uuid4()),
            "server_time": datetime.datetime.utcnow().isoformat(),
            "joined_text_length": len(" ".join(payload.responses))
        },
        "engine_output": result
    })
