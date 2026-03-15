import argparse
import sys

import requests
from rich.console import Console
from rich.table import Table

from model_manager import download_model

console = Console()
BASE_URL = "http://localhost:11435"


def cmd_serve(args):
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=11435, reload=True)


def cmd_list(args):
    try:
        resp = requests.get(f"{BASE_URL}/api/tags", timeout=5)
        data = resp.json()
        models = data.get("models", [])
    except requests.ConnectionError:
        console.print("[red]Server not running. Start it with: python cli.py serve[/red]")
        return
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return

    if not models:
        console.print("[yellow]No models found. Use 'pull' to download one.[/yellow]")
        return

    table = Table(title="Models")
    table.add_column("Name", style="cyan")
    table.add_column("Size (MB)", justify="right", style="green")
    table.add_column("Modified", style="dim")
    for m in models:
        table.add_row(
            m.get("name", "?"),
            str(m.get("size_mb", m.get("size", "?"))),
            m.get("modified", m.get("modified_at", "?")),
        )
    console.print(table)


def cmd_run(args):
    try:
        resp = requests.post(
            f"{BASE_URL}/api/generate",
            json={"model": args.model, "prompt": args.prompt, "stream": True},
            stream=True,
            timeout=10,
        )
        if resp.status_code == 404:
            data = resp.json()
            console.print(f"[red]{data.get('detail', 'Model not found')}[/red]")
            return
        for chunk in resp.iter_content(decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)
        print()
    except requests.ConnectionError:
        console.print("[red]Server not running. Start it with: python cli.py serve[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def cmd_pull(args):
    console.print(f"Downloading [cyan]{args.filename}[/cyan] from [cyan]{args.repo}[/cyan]...")
    try:
        path = download_model(args.repo, args.filename)
        console.print(f"[green]Model downloaded: {args.filename}[/green]")
    except Exception as e:
        console.print(f"[red]Download failed: {e}[/red]")


def cmd_delete(args):
    answer = console.input(f"Delete {args.model}? [y/N]: ")
    if answer.strip().lower() != "y":
        console.print("Cancelled.")
        return
    try:
        resp = requests.delete(
            f"{BASE_URL}/api/delete",
            json={"name": args.model},
            timeout=5,
        )
        if resp.status_code == 200:
            console.print(f"[green]Deleted {args.model}[/green]")
        elif resp.status_code == 404:
            console.print(f"[red]Model not found: {args.model}[/red]")
        else:
            console.print(f"[red]Error: {resp.text}[/red]")
    except requests.ConnectionError:
        console.print("[red]Server not running. Start it with: python cli.py serve[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def main():
    parser = argparse.ArgumentParser(prog="aat_llm", description="Local LLM server")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("serve", help="Start the server")

    subparsers.add_parser("list", help="List available models")

    run_parser = subparsers.add_parser("run", help="Run a model")
    run_parser.add_argument("model", help="Model filename (e.g. phi-2.Q4_K_M.gguf)")
    run_parser.add_argument("prompt", help="Prompt text")

    pull_parser = subparsers.add_parser("pull", help="Pull a model from HuggingFace")
    pull_parser.add_argument("repo", help="HuggingFace repo (e.g. TheBloke/phi-2-GGUF)")
    pull_parser.add_argument("filename", help="GGUF filename (e.g. phi-2.Q4_K_M.gguf)")

    del_parser = subparsers.add_parser("delete", help="Delete a model")
    del_parser.add_argument("model", help="Model filename to delete")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "serve": cmd_serve,
        "list": cmd_list,
        "run": cmd_run,
        "pull": cmd_pull,
        "delete": cmd_delete,
    }
    try:
        commands[args.command](args)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
