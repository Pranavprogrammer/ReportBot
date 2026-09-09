import argparse
from reportbot.database import get_summary

parser = argparse.ArgumentParser(description="ReportBot pipeline health")
parser.add_argument("--status", action="store_true", help="Show pipeline status")
args = parser.parse_args()

if args.status:
    s = get_summary()
    print("REPORTBOT STATUS")
    print("----------------")
    print(f"Total runs:        {s['total_runs']}")
    print(f"Successful runs:   {s['successful_runs']}")
    print(f"Rows processed:    {s['rows_processed']}")
    print(f"Last run:          {s['last_run']}")
