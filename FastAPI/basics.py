from collections.abc import Callable
import os
import asyncio

IntStringFloatTuple = tuple[int, str, float]

l: list[int] = [1, 2, 3, 4, 5]
t:IntStringFloatTuple = (1, "hello", 3.14)
s: set[int] = {1, 2, 3, 4, 5}
d: dict[str, int] = {"a": 1, "b": 2, "c": 3}

######################################################

ConditionFunction = Callable[[int], bool]
def filter_list(l: list[int], condition: ConditionFunction) -> list[int]:
    return [i for i in l if condition(i)]
def is_even(i: int) -> bool: return i % 2 == 0
print(filter_list( range (3,40), is_even))
######################################################


# ASYNC I/O
'''
Basically, this is a way to make I/O operations non-blocking and allow the program to perform other tasks while the read or write operation is ongoing
I/O operations are slow
- reading from disk
- network request
'''

with open(os.path.join(os.path.dirname(__file__),'README.md'),'r') as f:
    data  = f.read()
# The program will block here until the data has been read
# 99% percent of the execution time of the program is spent on waiting for the disk.
print(data)

'''
scenario:
- person 1 request for DB waits for 10 mins if
- second request comes have to wait


TO SOlve this in python web servers comes  "Web Server Gateway Interface (WSGI)" such as Flask, spawn serveral workers.

Those are sub-process of the web server that are all able to answer request,if one is busy other one will take it p

With asynchronous I/O, a single process won't block when processing a request with a long I/O operation.
While it waits for this operation to finish, it can answer other requests.
When the I/O operation is done, it resumes the request logic and can finally answer the request.

Technically, this is achieved through the concept of an `EVENT LOOP`.

Think of it as a conductor that will manage all the asynchronous tasks you send to it.
When data is available or when the write operation is done for one of those tasks, it'll ping the main program so that it can perform the next operations.

Underneath, it relies upon the OS select and poll calls, which are precisely there to ask for events about I/O operations at the operating system level.

After Intro `async` and `await`. so FastAPI is the successor and leverage paradigm  "Asynchronous Server Gateway Interface (ASGI)"
'''


async def amain():
    print("Hello ...")
    await asyncio.sleep(2)  #co-routine
    # we want to wait for this co-routine to finish before proceeding
    # if we omitted await, the coroutine obj would have been created but never executed
    print("... World!")

# entry point for async program
asyncio.run(amain()) # create-new event loop execute your code and return result


'''
add `async` to `def` this allow `await` keyword inside it. such async functions are called `COROUTINES`
'''

########################################################################################


async def printer(name: str, times: int) -> None:
        '''
        printer co-routine::
        function have async and await
        '''
        for _ in range(times):
                print(name)
                await asyncio.sleep(1)
                # if we remove await here, then "AAABBB"

async def main():
        '''
        asyncio.gather utility, which schedule several co-routines for concurrent execution
        '''
        await asyncio.gather(
                printer("A", 3),
                printer("B", 3),
        )

# entry-point create event-loop
asyncio.run(main())
