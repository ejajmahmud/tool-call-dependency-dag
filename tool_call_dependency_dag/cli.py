"""CLI for tool-call-dependency-dag."""
import sys
import argparse
from .dag import ToolDependencyDAG


def main():
    parser = argparse.ArgumentParser(description="Tool Call Dependency DAG")
    parser.add_argument("--demo", action="store_true", help="Run DAG scheduling demonstration")
    args = parser.parse_args()

    dag = ToolDependencyDAG()
    if args.demo:
        dag.add_tool_step("user_id", lambda ctx: 101, depends_on=[])
        dag.add_tool_step("profile", lambda ctx: f"Profile for {ctx['user_id']}", depends_on=["user_id"])
        dag.add_tool_step("billing", lambda ctx: f"Billing for {ctx['user_id']}", depends_on=["user_id"])
        dag.add_tool_step("summary", lambda ctx: f"{ctx['profile']} | {ctx['billing']}", depends_on=["profile", "billing"])

        print("Execution Waves:", dag.get_execution_waves())
        print("DAG Results:", dag.execute())
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
