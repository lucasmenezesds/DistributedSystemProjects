"""Simple reader-writer locks in Python
Many readers can hold the lock XOR one and only one writer"""
import threading

# version = """$Id: 04-1.html,v 1.3 2006/12/05 17:45:12 majid Exp $"""


class RWLock:
    """
A simple reader-writer lock Several readers can hold the lock
simultaneously, XOR one writer. Write locks have priority over reads to
prevent write starvation.
"""
    def __init__(self):
        self.rwlock = 0
        self.writers_waiting = 0
        self.monitor = threading.Lock()
        self.readers_ok = threading.Condition(self.monitor)
        self.writers_ok = threading.Condition(self.monitor)

    def acquire_read(self):
        """Acquire a read lock. Several threads can hold this typeof lock.
It is exclusive with write locks."""
        self.monitor.acquire()
        while self.rwlock < 0 or self.writers_waiting:
            self.readers_ok.wait()
        self.rwlock += 1
        self.monitor.release()

    def acquire_write(self):
        """Acquire a write lock. Only one thread can hold this lock, and
only when no read locks are also held."""
        self.monitor.acquire()
        while self.rwlock != 0:
            self.writers_waiting += 1
            self.writers_ok.wait()
            self.writers_waiting -= 1
        self.rwlock = -1
        self.monitor.release()

    def promote(self):
        """Promote an already-acquired read lock to a write lock
        WARNING: it is very easy to deadlock with this method"""
        self.monitor.acquire()
        self.rwlock -= 1
        while self.rwlock != 0:
            self.writers_waiting += 1
            self.writers_ok.wait()
            self.writers_waiting -= 1
        self.rwlock = -1
        self.monitor.release()

    def demote(self):
        """Demote an already-acquired write lock to a read lock"""
        self.monitor.acquire()
        self.rwlock = 1
        self.readers_ok.notifyAll()
        self.monitor.release()

    def release(self):
        """Release a lock, whether read or write."""
        self.monitor.acquire()
        if self.rwlock < 0:
            self.rwlock = 0
        else:
            self.rwlock -= 1
        wake_writers = self.writers_waiting and self.rwlock == 0
        wake_readers = self.writers_waiting == 0
        self.monitor.release()
        if wake_writers:
            self.writers_ok.acquire()
            self.writers_ok.notify()
            self.writers_ok.release()
        elif wake_readers:
            self.readers_ok.acquire()
            self.readers_ok.notifyAll()
            self.readers_ok.release()

# if __name__ == '__main__':
#     import time
#     rwl = RWLock()
#     class Reader(threading.Thread):
#         def run(self):
#             print self, 'start'
#             rwl.acquire_read()
#             print self, 'acquired'
#             time.sleep(5)
#             print self, 'stop'
#             rwl.release()

#     class Writer(threading.Thread):
#         def run(self):
#             print self, 'start'
#             rwl.acquire_write()
#             print self, 'acquired'
#             time.sleep(10)
#             print self, 'stop'
#             rwl.release()

#     class ReaderWriter(threading.Thread):
#         def run(self):
#             print self, 'start'
#             rwl.acquire_read()
#             print self, 'acquired'
#             time.sleep(5)
#             rwl.promote()
#             print self, 'promoted'
#             time.sleep(5)
#             print self, 'stop'
#             rwl.release()

#     class WriterReader(threading.Thread):
#         def run(self):
#             print self, 'start'
#             rwl.acquire_write()
#             print self, 'acquired'
#             time.sleep(10)
#             print self, 'demoted'
#             rwl.demote()
#             time.sleep(10)
#             print self, 'stop'
#             rwl.release()
#     # Reader().start()
#     # time.sleep(1)
#     # Reader().start()
#     # time.sleep(1)
#     # ReaderWriter().start()
#     # time.sleep(1)
#     # WriterReader().start()
#     # time.sleep(1)
#     # Reader().start()



# # import threading

# # __author__ = "Mateusz Kobos"
# # # http://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers/

# # class RWLock:
# #         """Synchronization object used in a solution of so-called second
# #         readers-writers problem. In this problem, many readers can simultaneously
# #         access a share, and a writer has an exclusive access to this share.
# #         Additionally, the following constraints should be met:
# #         1) no reader should be kept waiting if the share is currently opened for
# #                 reading unless a writer is also waiting for the share,
# #         2) no writer should be kept waiting for the share longer than absolutely
# #                 necessary.

# #         The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7]
# #         with a modification -- adding an additional lock (C{self.__readers_queue})
# #         -- in accordance with [2].

# #         Sources:
# #         [1] A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008
# #         [2] P.J. Courtois, F. Heymans, D.L. Parnas:
# #                 "Concurrent Control with 'Readers' and 'Writers'",
# #                 Communications of the ACM, 1971 (via [3])
# #         [3] http://en.wikipedia.org/wiki/Readers-writers_problem
# #         """

# #         def __init__(self):
# #                 self.__read_switch = _LightSwitch()
# #                 self.__write_switch = _LightSwitch()
# #                 self.__no_readers = threading.Lock()
# #                 self.__no_writers = threading.Lock()
# #                 self.__readers_queue = threading.Lock()
# #                 """A lock giving an even higher priority to the writer in certain
# #                 cases (see [2] for a discussion)"""

# #         def reader_acquire(self):
# #                 self.__readers_queue.acquire()
# #                 self.__no_readers.acquire()
# #                 self.__read_switch.acquire(self.__no_writers)
# #                 self.__no_readers.release()
# #                 self.__readers_queue.release()

# #         def reader_release(self):
# #                 self.__read_switch.release(self.__no_writers)

# #         def writer_acquire(self):
# #                 self.__write_switch.acquire(self.__no_readers)
# #                 self.__no_writers.acquire()

# #         def writer_release(self):
# #                 self.__no_writers.release()
# #                 self.__write_switch.release(self.__no_readers)


# # class _LightSwitch:
# #         """An auxiliary "light switch"-like object. The first thread turns on the
# #         "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
# #         def __init__(self):
# #                 self.__counter = 0
# #                 self.__mutex = threading.Lock()

# #         def acquire(self, lock):
# #                 self.__mutex.acquire()
# #                 self.__counter += 1
# #                 if self.__counter == 1:
# #                         lock.acquire()
# #                 self.__mutex.release()

# #         def release(self, lock):
# #                 self.__mutex.acquire()
# #                 self.__counter -= 1
# #                 if self.__counter == 0:
# #                         lock.release()
# #                 self.__mutex.release()