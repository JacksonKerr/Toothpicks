# Toothpicks

A coding challenge question from my course at the University of Otago.

Toothpicks.py By Jackson Kerr
    run with python3 Toothpicks.py <Generation> [Generational Ratio]
    Produces a representation of an nth generation toothpick diagram
    on the screen suitably scaled to fit the window.
    Gen 1 = a single horizontal toothpick.
    Generation n:
        For each toothpick in generation n-1 that has not had toothpicks 
        added to it, place two more toothpicks, each being perpendicular 
        to the original, and touching its ends at their midpoints.
    The optional second parameter represents the ratio of the length of 
    the toothpicks in each succeeding generation (ie. r = 0.8 means each 
    toothpick would be 0.8x as long as those in the previous generation).
    Args:
        -c Draw toothpicks in random colours
        -s Keep window open for only 5 seconds
