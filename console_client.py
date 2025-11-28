from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from warhead.core import WarheadSystem
import time
import argparse


def render_table(events):
    table = Table(title="WARHEAD SYSTEM — REAL-TIME FIRE LOG", expand=True)
    table.add_column("TIME", style="cyan", justify="right")
    table.add_column("EVENT", style="yellow")
    table.add_column("DETAILS", style="white")

    for t, ev, details in events[-10:]:  # Show last 10 events
        table.add_row(t, ev, details)

    return table


def main(max_count: int = 0):
    ws = WarheadSystem()
    events = []

    try:
        with Live(refresh_per_second=4) as live:
            count = 0
            while True:
                event = ws.tick()
                if event:
                    events.append(event)
                live.update(
                    Panel(render_table(events), title="WARHEAD: GATLING SIMULATION", border_style="red")
                )
                time.sleep(1)
                count += 1
                if max_count and count >= max_count:
                    break
    except KeyboardInterrupt:
        print("Exiting — interrupted by user")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run console WARHEAD display")
    parser.add_argument("--count", "-n", type=int, default=0, help="Number of ticks to run (0 = infinite)")
    args = parser.parse_args()
    main(args.count)
