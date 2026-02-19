""" Dataclasses:
    Example code, that demonstrates the new `slots` and
    the `keyword-only` features of dataclasses.

    The slots option is invoked as a parameters to the dataclass decorator.

    Key-words are demonstrated 3 ways:
       *** as a parameters to @dataclass,
       *** as a parameters to field(),
       *** as a sentinel value

    Some of these constructs caused nasty Error cases for the representer.

    Using Slots=True Frozen=True with uninitialized variables via typehint
    in dataclasses causes a
    AttributeError: 'NoneType' object has no attribute '_fields'
    When the result is parsed by generic_visit(node).

    More error scenarios are commented/noted above the construct.

    # See the following dataclasses issues for more information
    # https://github.com/python/cpython/blob/main/Lib/dataclasses.py#L1015-L1029
    # https://github.com/python/cpython/issues/98247
    # https://github.com/python/cpython/issues/89529
    # https://github.com/python/cpython/issues/132946
    # https://github.com/python/cpython/issues/132559
    # https://github.com/python/cpython/issues/135797
    # https://github.com/python/cpython/issues/98247
"""

from dataclasses import dataclass, field, KW_ONLY


# Dataclasses from PEP and documentation examples.
# The below are all equivalent when run through the @dataclass
# decorator.
@dataclass
class C:
    ...


@dataclass()
class C:
    ...


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
           match_args=True, kw_only=False, slots=False, weakref_slot=False)
class C:
    ...


@dataclass
class C:
    pass

# Unassigned but annotated class attributes/created class
# __init__() parameters.
@dataclass
class Color:
    r: int
    g: int
    b: int


# Default values for the class attributes/created class
# __init__() parameters.
@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0


# Using InitVar as described in the docs.
# This normalizes out to <parameter> = None.
# This works only for the purposes of representing,
# and would not work if the transform was permanent.
@dataclass
class C_InitVar:
    i: int
    j: int | None = None
    database: InitVar[DatabaseType | None] = None

    def __post_init__(self, database):
        if self.j is None and database is not None:
            self.j = database.lookup('j')


# Dataclasses using dataclass.make_dataclass()
# Note the unassigned (but type-hinted) parameters,
# as well as field defaults.
my_dataclass = make_dataclass(
    "C",
    [("x", int), "y", ("z", int, field(default=5))],
    namespace={"add_one": lambda self: self.x + 1})


my_other_dataclass = make_dataclass(
    'D',
    [('x', int, field(default=None)),
     'y', str, field(default="a")
     ('z', int, field(default=5))],
    namespace={'add_one': lambda self: self.x + 1})



# From the `sgf_parsing` exercise
# Demonstrates the combined use of slots and kw_only as parameters to @dataclass
@dataclass(frozen=True, slots=True, kw_only=True)
class SgfTree:
    properties: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def _parse(input):
        properties = input.read_properties()
        children = []
        while input.expect(";"):
            children.append(SgfTree(properties=input.read_properties()))
        while input.expect("(", advance=False):
            children.append(_parse(input))
        return SgfTree(properties=properties, children=children)


# This Node() class demonstrates use of the KW_ONLY sentinel.
# It also demonstrates a mix of initialized and uninitialized variables.
# (See node_id and children). This case used to fail with a
# "node has no ._fields attribute" error.
# Now the normalizer code inserts None for unassigned (but type-hinted) attributes.
# This would be a problem if this was a permanent transform, but is fine for
# the purposes of grouping representations, since we retain the students original code.
@dataclass
class Node:
    node_id: int # <--unassigned but type-hinted.
    _: KW_ONLY  # ***
    children: list = field(default_factory=list)

    def BuildTree(records):
        records.sort()

        # initialize one node for every record.
        trees = []
        for record in records:
            trees.append(Node(record.record_id))

        # match children to parents
        for record in records[1:]:
            parent = trees[record.parent_id]
            child = trees[record.record_id]
            parent.children.append(child)

        return trees[0]

# Variations on the above @dataclass parameters and attributes.
# This time using a filed object with a default factory
# (see the children attribute), with an unassigned but type-hinted
# attribute. The normalizer code assigns None to the
# attribute name and strips the type annotation.
@dataclass(frozen=True, slots=True, kw_only=True)
class SgfTree:
    properties: dict
    children: list = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class SgfTree:
    properties: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    name: str


@dataclass(frozen=True)
class SgfTree:
    children: list = field(default_factory=list)
    properties: int


@dataclass(kw_only=True)
class SgfTree:
    properties: dict
    children: list = field(default_factory=list)


@dataclass(slots=True)
class SgfTree:
    name: str
    properties: dict = field(default_factory=dict)
    children: list = field(default_factory=list)


@dataclass(kw_only=True)
class SgfTree:
    properties: dict
    children: list = field(default_factory=list)


@dataclass(init=False)
class ArgHolder:
    args: List[Any]
    kwargs: Mapping[Any, Any]

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


@dataclass
class Node:
    node_id: int
    _: KW_ONLY  # ***
    children: list = field(default_factory=list)


# These cases use Ellipsis to avoid explicit typehints in empty dataclass attributes.
# This ends up with Ellipsis being the type annotation:
# AnnAssign(target=Name(id='properties', ctx=Store()),
#           annotation=Constant(value=Ellipsis))
# The normalizer then creates a plain Assign that omits the typehint
# but assigns None as a value for the attribute name.
@dataclass(frozen=True, slots=True, kw_only=True)
class SgfTree:
    properties: ...
    children: list = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class SgfTree:
    properties: ... = 12
    children: list = field(default_factory=list)
    name: str


@dataclass
class Point:
    x: float = 0.0
    y: ...


# For some reason, this is still valid code.  However, when the
# ast is run, the annotation fields are assigned Ellipsis
# and None respectively. The value field is not present in the ast.
# This becomes normalized as <parameter> = None, with typehints removed.
@dataclass
class Color:
    r: ...
    g: None
    b: ...


# From the `tree_building` exercise.
# The Records() class demonstrates slots and kw_only as a field() parameter.
# But also has in uninitialized variable
@dataclass(slots=True)
class Record:
    record_id: int
    parent_id: int = field(kw_only=True)
    name: str

    def __lt__(self, other):
        return self.record_id < other.record_id


# From `go_counting` exercise.
# Demonstrates the use of slots for all variables.
# This exercise also demonstrates uninitialized variables.
# See x and y.
@dataclass(unsafe_hash=True, slots=True)
class Point:
    x: int
    y: int

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y)

    def __eq__(self, o):
        if isinstance(o, Point):
            return self.x == o.x and self.y == o.y
        return self.x == o[0] and self.y == o[1]


# From `word search`.  This is the case that prompted fixes for dataclass
# in the first place.  See forum post here:
# https://forum.exercism.org/t/my-solution-for-word-search-is-not-showing-up/11515/12
@dataclass
class Point:
    x: int
    y: int

class WordSearch:
    def __init__(self, puzzle: list[str]):
        self.puzzle, self.xmax, self.ymax = puzzle, len(puzzle[0]), len(puzzle)

    def search(self, word: str) -> tuple[Point, Point] | None:
        w = len(word) - 1
        for y, row in enumerate(self.puzzle):
            x = -1
            while (x := row.find(word[0], x + 1)) >= 0:
                for dx, dy in DIRS:
                    if 0 <= x + dx * w < self.xmax and 0 <= y + dy * w < self.ymax:
                        if all(self.puzzle[y + n * dy][x + n * dx] == ch for n, ch in enumerate(word)):
                            return Point(x, y), Point(x + dx * w, y + dy * w)

        return None
