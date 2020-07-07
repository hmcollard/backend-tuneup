#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Haley Collard"

import cProfile
import pstats
from pstats import SortKey
import functools
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        p = pstats.Stats(pr)
        p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(10)
        return result

    return wrapper


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    origionals = []
    duplicates = []
    [origionals.append(movie) if movie not in origionals else duplicates.append(movie) for movie in movies]
    # while movies:
    #     movie = movies.pop()
    #     if movie in movies:
    #         duplicates.append(movie)
    # while movies:
    #     if is_duplicate(movie, movies):
    #         duplicates.append(movie)
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(stmt="""find_duplicate_movies('movies.txt')""",
                     setup="""from __main__ import find_duplicate_movies""")
    result = t.repeat(repeat=7, number=5)
    smallest = min(result)
    best_time = smallest / 5
    print(f'Best time across 7 repeats of 5 runs per repeat: {best_time} sec')


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))
    timeit_helper()


if __name__ == '__main__':
    main()
