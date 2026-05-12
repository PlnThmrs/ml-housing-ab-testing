import logging
import os

from huggingface_hub import hf_hub_download

logger = logging.getLogger("uvicorn.error")


def _repo_id() -> str:
    repo_id = os.getenv("HF_REPO_ID", "")
    if not repo_id:
        raise ValueError("La variable HF_REPO_ID est manquante.")
    return repo_id


def _token() -> str | None:
    return os.getenv("HF_TOKEN") or None


def _download_file(filename: str, local_path: str) -> str:
    local_dir = os.path.dirname(local_path)
    os.makedirs(local_dir, exist_ok=True)
    hf_hub_download(
        repo_id=_repo_id(),
        filename=filename,
        repo_type="model",
        token=_token(),
        local_dir=local_dir,
    )
    return local_path


def download_model_from_hf() -> str:
    return _download_file(
        os.getenv("MODEL_OBJECT_NAME", "model_latest.joblib"),
        os.getenv("LOCAL_MODEL_PATH", "/app/artifacts/models/model_latest.joblib"),
    )


def download_ab_models_from_hf() -> dict:
    base = os.path.dirname(
        os.getenv("LOCAL_MODEL_PATH", "/app/artifacts/models/model_latest.joblib")
    )
    return {
        "A": _download_file(
            os.getenv("MODEL_A_OBJECT_NAME", "model_v1.joblib"),
            os.path.join(base, "model_v1.joblib"),
        ),
        "B": _download_file(
            os.getenv("MODEL_B_OBJECT_NAME", "model_v2.joblib"),
            os.path.join(base, "model_v2.joblib"),
        ),
    }
