# threadz 💨
## A cute Python library for better threading management

## Installation

- Clone the repo
- Run `python setup.py install`

## Usage

```python
import threadz
import time

def huge_calcul(n: int) -> int:
    """ A function that takes a long time to compute """
    time.sleep(1)
    return n**2

"""
List of tasks.

Task must be a tuple containing the target
function as the first element, and a tuple
of arguments as the second element.
"""

tasks = [
    (huge_calcul, (i,)) 
    for i in range(50)
]

"""
Most basic usage, run all the task in parallel.
The number of concurrent tasks is limited to 5
"""
threadz.run(tasks, concurrency=5) 


"""
Same as the example above, but we gather what the
function returns in a dictionnary.

The return value is a dictionary mapping task index 
to the results. If the function raises an exception,
the task index value is set to the exception.

This is also typing friendly, which means that if the
function must return an integer value, gather()
will return a dictionary with integers as values.
"""

results = threadz.gather(tasks, concurrency=5)

for r in results:
    print(r)


""" Last usage above... """
@threadz.threadify
def function():
    ...

function() # new thread will be created
function() # new thread will be created
function() # new thread will be created

```