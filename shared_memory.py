from multiprocessing import shared_memory, Process

'''
The parent process starts a library and writes an opening message in a shared notebook. 
The child process updates the notebook with new information.
'''

def librarian(shared_name):
    # Attach to the existing shared memory
    shm = shared_memory.SharedMemory(name=shared_name)
    # Write data to shared memory
    print("Child: Adding a new book to the library catalog...")
    shm.buf[:18] = b"New book: Python 101"
    shm.close()

if __name__ == "__main__":
    print("Parent: Setting up the library...")
    # Create shared memory
    shm = shared_memory.SharedMemory(create=True, size=128)
    
    # Parent writes initial data
    shm.buf[:14] = b"Library Opened!"
    print(f"Parent: Initial message - {bytes(shm.buf[:14]).decode()}")

    # Create a child process (assistant librarian)
    assistant = Process(target=librarian, args=(shm.name,))
    assistant.start()
    assistant.join()

    # Parent reads updated data
    print(f"Parent: Updated catalog - {bytes(shm.buf[:18]).decode()}")

    # Cleanup shared memory
    shm.close()
    shm.unlink()
    print("Parent: Library is closing.")
