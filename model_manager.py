import os
from pathlib import Path
from datetime import datetime, timezone

from huggingface_hub import hf_hub_download


def download_model(repo_id: str, filename: str, dest_dir: str = "./models") -> str:
    """Download a GGUF file from HuggingFace. Returns local file path."""
    os.makedirs(dest_dir, exist_ok=True)
    path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=dest_dir)
    return path


def list_models(models_dir: str = "./models") -> list[dict]:
    """Return list of dicts: { name, size_mb, modified }"""
    models_path = Path(models_dir)
    if not models_path.exists():
        return []
    result = []
    for f in sorted(models_path.glob("*.gguf")):
        stat = f.stat()
        result.append({
            "name": f.name,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        })
    return result


def delete_model(name: str, models_dir: str = "./models") -> bool:
    """Delete a model file. Returns True if deleted, False if not found."""
    if "/" in name or "\\" in name:
        raise ValueError(f"Invalid model name: {name}")
    path = Path(models_dir) / name
    if not path.exists():
        return False
    path.unlink()
    return True
