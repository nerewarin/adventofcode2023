"""
--- Day 25: Snowverload ---
https://adventofcode.com/2023/day/25
"""
import collections
import dataclasses
import traceback
from collections import defaultdict
from copy import deepcopy
from itertools import combinations

import numpy as np
import pulp
import networkx as nx
from networkx import NetworkXUnbounded

from utils.input_formatters import cast_2d_list_elements
from utils.position_search_problem import PositionSearchProblem
from utils.test_and_run import run, test


@dataclasses.dataclass
class Hailstone:
    position: tuple[int]
    velocity: tuple[int]
    name: str

    def __post_init__(self):
        assert len(self.position) == len(self.velocity)
        self.x, self.y, self.z = self.position
        self.vx, self.vy, self.vz = self.velocity

    def update_pos(self, new_pos):
        self.position = new_pos
        self.x, self.y, self.z = self.position

    @classmethod
    def from_line(cls, line, line_num):
        return cls(*(tuple(int(s) for s in side.split(",")) for side in line.split("@")), chr(65 + line_num))

    @property
    def shape(self):
        return len(self.position)

    @staticmethod
    def find_intersection_point(hailstone1, hailstone2, test_area):
        x1, y1, _ = hailstone1.position
        vx1, vy1, _ = hailstone1.velocity
        x2, y2, _ = hailstone2.position
        vx2, vy2, _ = hailstone2.velocity

        # Checking if the velocity vectors are parallel (no intersection if parallel)
        if vy1 * vx2 == vx1 * vy2:
            return None

        # Calculating intersection point
        # System of equations:
        # x1 + vx1 * t1 = x2 + vx2 * t2
        # y1 + vy1 * t1 = y2 + vy2 * t2
        # We solve for t1 and t2
        denominator = vx2 * vy1 - vx1 * vy2
        if denominator == 0:
            return None  # Lines are parallel, no intersection

        dx = x2 - x1
        dy = y2 - y1

        t1 = (dy * vx2 - dx * vy2) / denominator
        t2 = (dy * vx1 - dx * vy1) / denominator

        # Check if t1 and t2 are non-negative
        if t1 < 0 or t2 < 0:
            return None

        # Intersection point
        intersect_x = x1 + vx1 * t1
        intersect_y = y1 + vy1 * t1

        # Check if intersection is within the test area
        if test_area[0] <= intersect_x <= test_area[1] and test_area[0] <= intersect_y <= test_area[1]:
            return (intersect_x, intersect_y), t1, t2

        return None


class Snowverload:
    def __init__(self, inp, area=None):
        self.area = area
        self.graph, self.nx_graph = self._parse_input(inp)

    @staticmethod
    def _parse_input(inp):
        nx_graph = nx.Graph()

        graph = defaultdict(set)
        for line in inp:
            node, neighbors = line.split(":")
            neighbors = [n.strip() for n in neighbors.split()]

            nx_graph.add_node(node)

            for neighbor in neighbors:
                graph[node].add(neighbor)
                graph[neighbor].add(node)

                nx_graph.add_node(neighbor)
                nx_graph.add_edge(node, neighbor)

        return graph, nx_graph

    def disconnect_and_multiply(self):
        graph = self.nx_graph
        assert len(graph.nodes) == len(self.graph)

        def check_disconnection(graph, edges_to_remove):
            H = graph.copy()
            H.remove_edges_from(edges_to_remove)
            # Check if the graph is disconnected and forms two components
            if nx.is_connected(H):
                return False
            components = list(nx.connected_components(H))
            assert len(components) == 2
            return [len(subgraph) for subgraph in components]

        # Iterate over all combinations of three edges
        total_edges = 53546395200
        # 53,546,395,200
        i = 0
        for edges in combinations(graph.edges(), 3):
            i += 1
            if not i % 1e9:
                print(i)

            if numbers := check_disconnection(graph, edges):
                print("Edges to remove:", edges)
                return numbers[0] * numbers[1]

        raise ValueError("no solution found")

    def disconnect_and_multiply2(self):
        G = self.nx_graph # .to_directed()
        # nx.set_edge_attributes(G, 1, 'capacity')
        nodes = list(G.nodes)

        def find_edges_to_disconnect(G_original):
            centrality = nx.edge_betweenness_centrality(G_original)
            sorted_edges = sorted(G_original.edges(), key=lambda edge: centrality[edge], reverse=True)

            # Try removing sets of three edges
            i = 0
            for edges in combinations(sorted_edges, 3):
                i += 1
                if not i % 1e9:
                    print(i)

                # Create a copy of the graph for each trial
                G = G_original.copy()
                G.remove_edges_from(edges)

                # Check if the graph is now disconnected into two components of specific sizes
                if nx.is_connected(G):
                    continue

                components = list(nx.connected_components(G))
                if len(components) == 2:
                    return len(components[0]) * len(components[1])

            return None


        # for i, j in combinations(range(len(nodes)), 2):
        #     source = nodes[i]
        #     sink = nodes[j]
        #
        #     try:
        #         return find_minimum_cuts(G, 3)
        #     except (NetworkXUnbounded, ValueError) as exc:
        #         print(f"{sink=}, {source=}, {exc}")
        #         continue

        return find_edges_to_disconnect(G)


def snowverload(inp, part=1, area=None):
    if part == 1:
        return Snowverload(inp).disconnect_and_multiply2()

    # return Snowverload(inp).get_sum_of_rock_coordinate()


if __name__ == "__main__":
    test(snowverload, expected=54)
    run(snowverload)
