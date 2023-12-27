"""
--- Day 19: Aplenty  ---
https://adventofcode.com/2023/day/19
"""
import dataclasses
from operator import gt, lt
from typing import Callable

from utils.test_and_run import run, test


@dataclasses.dataclass
class Clause:
    attr: str
    comparator: Callable
    arg: int
    output: str


@dataclasses.dataclass
class Workflow:
    name: str
    clauses: list[Clause]
    fallback: str
    workflow_by_name: dict[str, "Workflow"] = None

    @classmethod
    def from_line(cls, line):
        name, _schema = line.split("{")
        assert _schema[-1] == "}"
        schemas = _schema[:-1].split(",")
        fallback = schemas[-1]

        clauses = []
        for schema in schemas[:-1]:
            raw_clause, output = schema.split(":")
            if ">" in raw_clause:
                comparator = gt
                comparator_str = ">"
            elif "<" in raw_clause:
                comparator = lt
                comparator_str = "<"
            else:
                raise ValueError(f"no comparator found in {raw_clause}")

            attr, arg = raw_clause.split(comparator_str)
            clause = Clause(attr, comparator, int(arg), output)
            clauses.append(clause)

        return cls(name, clauses, fallback)

    def run(self, part):
        for clause in self.clauses:
            value = part[clause.attr]
            comparator_result = clause.comparator(value, clause.arg)
            if comparator_result:
                return clause.output
        return self.fallback

    def _add_clause(self, existing, new, operator):
        # adds new clause to existing using and/or operator
        if not existing:
            return new

        a = 0

    def get_acceptance_clause(self):
        comparator_to_str = {
            gt: ">",
            lt: "<",
        }

        full_acceptance_clause = ""
        next_operator = None
        for clause in self.clauses:

            attr = clause.attr
            comparator_str = comparator_to_str[clause.comparator]
            arg = clause.arg
            clause_str = f"part[{attr!r}] {comparator_str} {arg}"

            if clause.output == "A":
                full_acceptance_clause = self._add_clause(full_acceptance_clause, clause_str, next_operator)
                next_operator = "or"
            elif clause.output == "R":
                clause_str = f"not {clause_str}"
                full_acceptance_clause = self._add_clause(full_acceptance_clause, clause_str, next_operator)
                next_operator = "or"
            else:
                acceptance = "and " + self.workflow_by_name[clause.output].get_acceptance_clause()

            a = 0

        # add fallback
        if self.fallback == "R":
            a = 0
            pass
        elif self.fallback == "A":
            a = 0
            pass
        else:
            w_fallback = self.workflow_by_name[self.fallback]
            fallback_clause_str = w_fallback.get_acceptance_clause()
            full_acceptance_clause = self._add_clause(full_acceptance_clause, fallback_clause_str, next_operator)

        return full_acceptance_clause

class Part(dict):
    @classmethod
    def from_line(cls, line):
        data = {}
        for part in line[1:-1].split(","):
            k, v = part.split("=")
            data[k] = int(v)

        return cls(data)


class Aplenty:
    def __init__(self, inp):
        self.raw_inp = inp
        self.workflows, self.parts = self._parse_input(inp)

        self.workflow_by_name = {
            w.name: w for w in self.workflows
        }
        for w in self.workflows:
            w.workflow_by_name = self.workflow_by_name

    @staticmethod
    def _parse_input(inp):
        part = 1
        workflows = []
        parts = []
        for line in inp:
            if not line:
                part = 2
                continue

            if part == 1:
                workflows.append(Workflow.from_line(line))
            if part == 2:
                parts.append(Part.from_line(line))

        return workflows, parts

    def get_sum_of_accepted_parts_ratings(self):
        accepted_parts = []

        for part in self.parts:
            w_name = "in"
            while True:
                w = self.workflow_by_name[w_name]

                w_res = w.run(part)
                match w_res:
                    case "A":
                        accepted_parts.append(part)
                        break
                    case "R":
                        # rejected
                        break
                    case _:
                        w_name = w_res

        ratings = []
        for part in accepted_parts:
            ratings.append(sum(part.values()))

        return sum(ratings)

    def get_distinct_combinations_of_accepted_ratings(self):
        for w in self.workflows:
            clauses = w.get_acceptance_clause()
            a = 0

def aplenty(inp, part=1, **kw):
    if part == 1:
        return Aplenty(inp).get_sum_of_accepted_parts_ratings()
    Aplenty(inp).get_distinct_combinations_of_accepted_ratings()


if __name__ == "__main__":
    test(aplenty, 19114)
    assert run(aplenty) == 487623

    test(aplenty, part=2, expected=167409079868000)
    run(aplenty, part=2)
