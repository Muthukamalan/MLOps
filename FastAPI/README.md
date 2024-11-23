# FastAPI

Terminolgy:
- event loop
- co-routine
- async/await


<!-- 
scenario:
- person 1 request for DB waits for 10 mins if
- second request comes have to wait


TO SOlve this in python web servers comes  "Web Server Gateway Interface (WSGI)" such as Flask, spawn serveral workers.

Those are sub-process of the web server that are all able to answer request,if one is busy other one will take it.

With asynchronous I/O, a single process won't block when processing a request with a long I/O operation.
While it waits for this operation to finish, it can answer other requests.
When the I/O operation is done, it resumes the request logic and can finally answer the request.

Technically, this is achieved through the concept of an `EVENT LOOP`.

Think of it as a conductor that will manage all the asynchronous tasks you send to it.
When data is available or when the write operation is done for one of those tasks, it'll ping the main program so that it can perform the next operations.

Underneath, it relies upon the OS select and poll calls, which are precisely there to ask for events about I/O operations at the operating system level.

After Intro `async` and `await`. so FastAPI is the successor and leverage paradigm  "Asynchronous Server Gateway Interface (ASGI)"

add `async` to `def` this allow `await` keyword inside it. such async functions are called `COROUTINES`
-->

## ASYNC I/O
Basically, this is a way to make I/O operations non-blocking and allow the program to perform other tasks while the read or write operation is ongoing I/O operations are slow
- reading from disk
- network request

```
It's worth noting that FastAPI is built upon two main py libraries:
    - starlette: low-lvl ASGI web framework 
    - pydantic: data-validation library based on type hints
```

HTTP is a simple yet powerful technique for sending data to and receiving data from a server.


## Dependency Injection
it is a powerful and readable approach to reusing logic across your projec
usecase for dependencies:
- authentication system
- query parameter validator
- rate limiter

All dependency injection needs `Callable` Object

In FastAPI, a dependency injection can even call another one recursively, allowing you to build high-level blocks from basic features.



```
dependency injection is a system to automatically instantiate objects and the ones they depend on. The responsibility of developers is then to only provide a declaration of how an object should be created, and let the system resolve all the dependency chains and create the actual objects at runtime.
```


# websocket
As we said in the intro to this chapter, a typical use case for websocket is to implement real-time communication across mul

```
python -m http.server --directory WebSoc/echo 9000
```

