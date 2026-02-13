import heapq
from collections import deque
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass


@dataclass
class PuzzleState:
    """Represents a state of the 8-puzzle."""
    tiles: Tuple[int, ...]  # Immutable tuple for hashing
    moves: int  # Number of moves made to reach this state
    parent: 'PuzzleState' = None  # Parent state for path reconstruction
    move_description: str = ""  # Description of the move to reach this state

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(self.tiles)

    def __lt__(self, other):
        # For priority queue comparison
        return (self.moves + self.heuristic()) < (other.moves + other.heuristic())

    def heuristic(self) -> int:
        """
        Manhattan distance heuristic.
        Calculates the sum of distances of each tile from its goal position.
        """
        distance = 0
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # Goal state (0 = blank)
        
        for i in range(9):
            if self.tiles[i] != 0:  # Skip the blank tile
                current_row, current_col = i // 3, i % 3
                goal_pos = goal.index(self.tiles[i])
                goal_row, goal_col = goal_pos // 3, goal_pos % 3
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        
        return distance

    def is_goal(self) -> bool:
        """Check if puzzle is in goal state."""
        return self.heuristic() == 0

    def get_moves(self) -> List['PuzzleState']:
        """Generate all possible next states from current state."""
        next_states = []
        blank_pos = self.tiles.index(0)
        blank_row, blank_col = blank_pos // 3, blank_pos % 3
        
        # Possible moves: up, down, left, right
        directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }
        
        for direction, (dr, dc) in directions.items():
            new_row, new_col = blank_row + dr, blank_col + dc
            
            # Check if new position is valid
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_pos = new_row * 3 + new_col
                # Swap tiles
                tiles_list = list(self.tiles)
                tiles_list[blank_pos], tiles_list[new_pos] = tiles_list[new_pos], tiles_list[blank_pos]
                new_tiles = tuple(tiles_list)
                
                next_state = PuzzleState(
                    tiles=new_tiles,
                    moves=self.moves + 1,
                    parent=self,
                    move_description=direction
                )
                next_states.append(next_state)
        
        return next_states

    def display(self):
        """Display the puzzle in a readable format."""
        for i in range(9):
            if i % 3 == 0:
                print()
            if self.tiles[i] == 0:
                print("  _  ", end="")
            else:
                print(f"  {self.tiles[i]}  ", end="")
        print()


class EightPuzzleSolver:
    """Solver for the 8-puzzle using A* search algorithm."""

    def __init__(self, initial_tiles: List[int]):
        """Initialize solver with initial puzzle state."""
        if len(initial_tiles) != 9 or sorted(initial_tiles) != list(range(9)):
            raise ValueError("Invalid puzzle configuration")
        
        self.initial_state = PuzzleState(
            tiles=tuple(initial_tiles),
            moves=0,
            parent=None
        )
        self.goal_state = PuzzleState(tiles=(1, 2, 3, 4, 5, 6, 7, 8, 0), moves=0)
        self.explored = set()
        self.nodes_expanded = 0

    def solve(self) -> Tuple[bool, List[PuzzleState], int]:
        """
        Solve the puzzle using A* search algorithm.
        
        Returns:
            Tuple of (success, path_to_goal, nodes_expanded)
        """
        if self.initial_state.is_goal():
            return True, [self.initial_state], 0

        # Priority queue: (f_score, counter, state)
        # counter prevents ties and ensures FIFO for equal f-scores
        open_set = []
        counter = 0
        heapq.heappush(open_set, (self.initial_state.heuristic(), counter, self.initial_state))
        counter += 1
        
        visited = {self.initial_state}
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            self.explored.add(current)
            self.nodes_expanded += 1
            
            if current.is_goal():
                # Reconstruct path
                path = []
                node = current
                while node is not None:
                    path.append(node)
                    node = node.parent
                path.reverse()
                return True, path, self.nodes_expanded
            
            # Explore neighbors
            for next_state in current.get_moves():
                if next_state not in visited:
                    visited.add(next_state)
                    f_score = next_state.moves + next_state.heuristic()
                    heapq.heappush(open_set, (f_score, counter, next_state))
                    counter += 1
        
        return False, [], self.nodes_expanded

    def print_solution(self):
        """Solve and print the solution path."""
        success, path, nodes_expanded = self.solve()
        
        print("=" * 50)
        print("8-PUZZLE SOLVER (A* with Manhattan Distance)")
        print("=" * 50)
        
        print("\nInitial State:")
        self.initial_state.display()
        
        if success:
            print(f"\n✓ Solution found!")
            print(f"Number of moves: {len(path) - 1}")
            print(f"Nodes expanded: {nodes_expanded}")
            
            print("\nSolution path:")
            for i, state in enumerate(path):
                if i > 0:
                    print(f"\nMove {i}: {state.move_description.upper()}")
                else:
                    print("\nInitial:")
                state.display()
        else:
            print(f"\n✗ No solution found!")
            print(f"Nodes expanded: {nodes_expanded}")
        
        print("\n" + "=" * 50)


def main():
    """Main function to test the 8-puzzle solver."""
    
    # Example 1: Simple puzzle (2 moves away from goal)
    print("\n" + "="#50 + "\n")
    print("EXAMPLE 1: Simple puzzle (2 moves from goal)")
    initial_state_1 = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    solver_1 = EightPuzzleSolver(initial_state_1)
    solver_1.print_solution()
    
    # Example 2: Medium difficulty puzzle
    print("\n" + "="#50 + "\n")
    print("EXAMPLE 2: Medium difficulty puzzle")
    initial_state_2 = [1, 2, 3, 4, 0, 5, 7, 8, 6]
    solver_2 = EightPuzzleSolver(initial_state_2)
    solver_2.print_solution()
    
    # Example 3: More complex puzzle
    print("\n" + "="#50 + "\n")
    print("EXAMPLE 3: More complex puzzle")
    initial_state_3 = [8, 7, 6, 5, 4, 3, 2, 1, 0]
    solver_3 = EightPuzzleSolver(initial_state_3)
    solver_3.print_solution()
    
    # Example 4: Already at goal
    print("\n" + "="#50 + "\n")
    print("EXAMPLE 4: Already at goal state")
    initial_state_4 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solver_4 = EightPuzzleSolver(initial_state_4)
    solver_4.print_solution()


if __name__ == "__main__":
    main()
