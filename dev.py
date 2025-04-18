import asyncio, time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FILES = {"index.html", "template.html"}
WATCHED_DIRS = {"src"}
COOLDOWN_SECONDS = 0.5


def should_watch(path: str):
    if any(path.endswith(f) for f in WATCHED_FILES):
        return True
    if any(path.startswith(f"{d}/") or f"/{d}/" in path for d in WATCHED_DIRS):
        return path.endswith(".md")
    return False


class RebuildHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_run = 0
        self.running = False

    def _trigger_if_valid(self, event):
        if self.running:
            return
        if not should_watch(event.src_path):
            return

        now = time.time()
        if now - self.last_run < COOLDOWN_SECONDS:
            return

        self.last_run = now
        print(f"\n[change made to {Path(event.src_path).name}]\nRebuilding..")
        asyncio.run(self.run_main_py())

    def on_modified(self, event):
        self._trigger_if_valid(event)

    def on_created(self, event):
        self._trigger_if_valid(event)

    def on_deleted(self, event):
        self._trigger_if_valid(event)

    async def run_main_py(self):
        self.running = True
        start = time.time()
        proc = await asyncio.create_subprocess_exec("python", "main.py")
        await proc.wait()
        end = time.time()
        print(f"Successfully rebuilt in {int((end - start) * 1000)}ms.\n")
        self.running = False


if __name__ == "__main__":
    event_handler = RebuildHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    print("Watching for changes... (Ctrl+C to quit)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
