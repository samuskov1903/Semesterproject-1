"""Manually defined navigation map for the robot course.

The node names match the red labels in the course drawing. Numbered nodes
are intersections, while a1-a5, b1-b5, p1, and p2 are endpoints.
a = red
b = white
p = pickup
"""


# Directions are relative to the robot's current orientation.  Each node can
# therefore have a straight, backward, left, and/or right route.
PATH_MAP = {
    "start": {"straight": "1"},
    "1": {"backward": "start", "straight": "2", "right": "18"},
    "2": {"backward": "1", "left": "3", "right": "15"},
    "3": {"backward": "2", "straight": "4", "left": "a1", "right": "b1"},
    "4": {"backward": "3", "straight": "5", "right": "b2"},
    "5": {"backward": "4", "straight": "10", "left": "a2"},
    "6": {"backward": "7", "straight": "8"},
    "7": {"backward": "6", "straight": "19"},
    "8": {"backward": "7", "straight": "13"},
    "9": {"backward": "10", "straight": "11", "left": "a3"},
    "10": {"backward": "5", "straight": "9", "right": "p2"},
    "11": {"backward": "9", "straight": "12"},
    "12": {"backward": "11", "right": "a4"},
    "13": {"backward": "8", "straight": "14", "right": "b3"},
    "14": {"backward": "13", "straight": "15", "right": "b4"},
    "15": {"backward": "14", "straight": "16", "left": "2"},
    "16": {"backward": "15", "straight": "17", "right": "a5"},
    "17": {"backward": "16", "straight": "18", "right": "p1"},
    "18": {"backward": "17", "left": "1", "straight": "19"},
    "19": {"backward": "18", "straight": "7", "right": "b5"},
    "a1": {"backward": "3"},
    "a2": {"backward": "5"},
    "a3": {"backward": "9"},
    "a4": {"backward": "12"},
    "a5": {"backward": "16"},
    "b1": {"backward": "3"},
    "b2": {"backward": "4"},
    "b3": {"backward": "13"},
    "b4": {"backward": "14"},
    "b5": {"backward": "19"},
    "p1": {"backward": "17"},
    "p2": {"backward": "10"},
}


class Navigation:
    """Track the robot's current node on the manually defined map."""

    def __init__(self, start="start"):
        if start not in PATH_MAP:
            raise ValueError("Unknown starting node: " + start)
        self.current_node = start

    def available_directions(self):
        """Return the directions available from the current node."""
        return PATH_MAP[self.current_node]

    def move(self, direction):
        """Move in a direction listed for the current node."""
        if direction not in PATH_MAP[self.current_node]:
            raise ValueError(
                "No " + direction + " path from " + self.current_node
            )
        self.current_node = PATH_MAP[self.current_node][direction]
        return self.current_node