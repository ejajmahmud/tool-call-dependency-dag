"""Tests for tool-call-dependency-dag."""
import unittest
from tool_call_dependency_dag.dag import ToolDependencyDAG


class TestToolDependencyDAG(unittest.TestCase):
    def setUp(self):
        self.dag = ToolDependencyDAG()

    def test_wave_ordering(self):
        self.dag.add_tool_step("a", lambda ctx: "a", depends_on=[])
        self.dag.add_tool_step("b", lambda ctx: "b", depends_on=["a"])
        self.dag.add_tool_step("c", lambda ctx: "c", depends_on=["b"])
        waves = self.dag.get_execution_waves()
        self.assertEqual(waves, [["a"], ["b"], ["c"]])
        res = self.dag.execute()
        self.assertEqual(res, {"a": "a", "b": "b", "c": "c"})

    def test_cycle_detection(self):
        self.dag.add_tool_step("x", lambda ctx: "x", depends_on=["y"])
        self.dag.add_tool_step("y", lambda ctx: "y", depends_on=["x"])
        with self.assertRaises(ValueError):
            self.dag.execute()


if __name__ == "__main__":
    unittest.main()
