def linrange(start, stop, n=10):
    '''generator for n evenly spaced numbers from start to stop

    Example:
    >>> list(linrange(2, 7, 5))
    [2.0, 3.25, 4.5, 5.75, 7.0]
    '''
    assert n > 0
    step = (stop-start)/(n-1) if n>1 else 0
    for i in range(n):
        yield start + i * step


def logrange(start, stop, n=10):
    '''generator for n logarithmically spaced numbers from start to stop

    Example:
    >>> list(logrange(10, 1000, 3))
    [10, 100.0, 1000.0]
    '''
    assert n > 0
    assert start > 0
    assert stop > 0
    factor = (stop/start)**(1/(n-1))
    x = start
    for i in range(n):
        yield x
        x *= factor
