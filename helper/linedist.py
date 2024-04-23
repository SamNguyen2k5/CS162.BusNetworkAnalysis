"""
Helper projecting functions.
"""

import math
import numpy as np

def proj(X, A, B) -> tuple[np.ndarray, float]:
    """
    Returns a tuple of
        - The point on the line segment AB that is closest to X, and
        - The smallest distance of that found point and the segment AB.
    """
    X = np.array(X)
    A = np.array(A)
    B = np.array(B)

    XA = A - X
    AB = B - A
    a = np.dot(AB, AB)
    b = 2 * np.dot(XA, AB)
    c = np.dot(XA, XA)

    if a == 0:      # A = B -> proj(X, AB) = A
        return A, math.sqrt(c)

    t = min(1.0, max(0.0, - b / (2 * a)))
    return A + t * AB, math.sqrt(max(0.0, a * t * t + b * t + c))

def proj_vector(X, A, B) -> np.ndarray:
    """
    Returns the point on the line segment AB that is closest to X.
    """
    return proj(X, A, B)[0]

def line_dist(X, A, B) -> float:
    """
    Returns the smallest distance of that found point and the segment AB.
    """
    return proj(X, A, B)[1]