from typing import List, NamedTuple, Dict, Optional, Literal, cast, get_args
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def log(*message: str):
    print(*message, file=sys.stderr)


ProteinType = Literal['A', 'B', 'C', 'D']
DirectionType = Literal['N', 'E', 'S', 'W']
OrganType = Literal['ROOT', 'BASIC', 'HARVESTER']
WALL: str = 'WALL'

width: int
height: int
width, height = [int(i) for i in input().split()]


class Pos(NamedTuple):
    x: int
    y: int


class Organ(NamedTuple):
    id: int
    owner: int
    parent_id: int
    root_id: int
    pos: Pos
    organ_type: OrganType
    dir: DirectionType


class Protein(NamedTuple):
    pos: Pos
    protein_type: ProteinType


class Cell(NamedTuple):
    pos: Pos
    isWall: bool = False
    protein: Optional[ProteinType] = None
    organ: Optional[Organ] = None


class Grid:
    cells: List[Cell] = []

    def __init__(self) -> None:
        self.reset()
    
    def reset(self) -> None:
        self.cells = []
        for y in range(height):
            for x in range(width):
                self.cells.append(Cell(Pos(x, y)))

    def get_cell(self, pos: Pos) -> Optional[Cell]:
        if width > pos.x >= 0 and height > pos.y >= 0:
            return self.cells[pos.x + width * pos.y]
        return None
    
    def set_cell(self, pos: Pos, cell: Cell) -> None:
        self.cells[pos.x + width * pos.y] = cell


class Game:
    grid: Grid
    my_proteins: Dict[ProteinType, int]
    opp_proteins: Dict[ProteinType, int]
    my_organs: List[Organ]
    opp_organs: List[Organ]
    free_proteins = List[Protein]
    organ_map: Dict[int, Organ]

    def __init__(self) -> None:
        self.grid = Grid()
        self.reset()

    def reset(self) -> None:
        self.my_proteins = {}
        self.opp_proteins = {}
        self.grid.reset()
        self.my_organs = []
        self.opp_organs = []
        self.free_proteins = []
        self.organ_map = {}


game: Game = Game()

def next_to(x1, y1, x2, y2):
    if x2 == x1 and y2 == y1 - 1:
        return 'N'  # North
    elif x2 == x1 and y2 == y1 + 1:
        return 'S'  # South
    elif x2 == x1 + 1 and y2 == y1:
        return 'E'  # East
    elif x2 == x1 - 1 and y2 == y1:
        return 'W'  # West
    else:
        return None  # Not adjacent or not a cardinal direction

counter = 0

# game loop
while True:
    game.reset()

    entity_count: int = int(input())
    for i in range(entity_count):
        inputs: List[str] = input().split()
        x: int = int(inputs[0])
        y: int = int(inputs[1])
        pos: Pos = Pos(x, y)
        _type: str = inputs[2]
        owner: int = int(inputs[3])
        organ_id: int = int(inputs[4])
        organ_dir: DirectionType = cast(DirectionType, inputs[5])
        organ_parent_id: int = int(inputs[6])
        organ_root_id: int = int(inputs[7])

        cell: Optional[Cell] = None
        organ: Optional[Organ] = None

        if _type == WALL:
            cell = Cell(pos, True)
        elif _type in get_args(ProteinType):
            cell = Cell(pos, False, cast(ProteinType, _type))
            protein = Protein(pos, _type)
            game.free_proteins.append(protein)
        else:
            organ = Organ(organ_id, owner, organ_parent_id, organ_root_id, pos, cast(OrganType, _type), organ_dir)
            cell = Cell(pos, False, None, organ)
            if owner == 1:
                game.my_organs.append(organ)
            else:
                game.opp_organs.append(organ)
            game.organ_map[organ_id] = organ
        
        if cell != None:
            game.grid.set_cell(pos, cell)

    my_proteins: List[int] = [int(i) for i in input().split()]
    opp_proteins: List[int] = [int(i) for i in input().split()]

    game.my_proteins = { 'A': my_proteins[0], 'B': my_proteins[1], 'C': my_proteins[2], 'D': my_proteins[3] }
    game.opp_proteins = { 'A': opp_proteins[0], 'B': opp_proteins[1], 'C': opp_proteins[2], 'D': opp_proteins[3] }

    required_actions_count: int = int(input())

    for i in range(required_actions_count):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        parents_id_list = []
        for organ in game.my_organs:
            parents_id_list.append(organ.parent_id)
        for organ in game.my_organs:
            if organ.id not in parents_id_list:
                my_last_organ = organ
                my_last_organ_id = organ.id

        my_last_organ_pos = my_last_organ.pos
        my_last_organ_x, my_last_organ_y = my_last_organ_pos.x, my_last_organ_pos.y

        opp_last_organ = game.opp_organs[-1]
        opp_last_organ_pos = opp_last_organ.pos
        opp_last_organ_x, opp_last_organ_y = opp_last_organ_pos.x, opp_last_organ_pos.y

        first_protein = game.free_proteins[0]
        first_protein_pos = first_protein.pos
        first_protein_x, first_protein_y = first_protein_pos.x, first_protein_pos.y

        if not next_to(my_last_organ_x, my_last_organ_y, first_protein_x-1, first_protein_y) and game.my_proteins['C'] != 0:
            print(f"GROW {my_last_organ_id} {first_protein_x-2} {first_protein_y} BASIC")
        elif game.my_proteins['C'] != 0:
            print(f"GROW {my_last_organ_id} {first_protein_x-1} {first_protein_y} HARVESTER E")
        elif not game.grid.get_cell(Pos(first_protein_x-1, first_protein_y+1)).isWall and counter == 0:
            counter += 1
            print(f"GROW {my_last_organ_id} {my_last_organ_x} {first_protein_y+1} BASIC")
        elif game.grid.get_cell(Pos(first_protein_x-1, first_protein_y+1)).isWall and counter == 0:
            counter += 1
            print(f"GROW {my_last_organ_id} {my_last_organ_x} {first_protein_y-1} BASIC")
        elif counter == 1 or counter == 2:
            counter += 1
            print(f"GROW {my_last_organ_id} {first_protein_x+1} {my_last_organ_y} BASIC")
        else:
            for opp_organ in game.opp_organs:
                opp_organ_pos = opp_organ.pos
                opp_organ_x, opp_organ_y = opp_organ_pos.x, opp_organ_pos.y
                if next_to(my_last_organ_x, my_last_organ_y, opp_organ_x, opp_last_organ_y):
                    counter += 1
            if counter == 3:
                for cell in game.grid.cells:
                    if not cell.isWall and not cell.protein and not cell.organ in game.opp_organs and not cell.organ in game.my_organs:
                        empty_cell_x, empty_cell_y = cell.pos.x, cell.pos.y
                        print(f"GROW {my_last_organ_id} {empty_cell_x} {empty_cell_y} BASIC")
                        break
            else:
                print(f"GROW {my_last_organ_id} {opp_last_organ_x} {opp_last_organ_y} BASIC")