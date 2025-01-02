import os
import multiprocessing

'''
The parent process gives the child process an order to prepare cookies, 
and the child sends back a message when it’s done.
'''

def baker(pipe_out):
    os.write(pipe_out, b"Cookies are ready!")
    os.close(pipe_out)

if __name__ == "__main__":
    print("Parent: Welcome to the bakery!")
    # Create a pipe
    pipe_in, pipe_out = os.pipe()

    # Create a child process (the assistant baker)
    assistant = multiprocessing.Process(target=baker, args=(pipe_out,))
    assistant.start()

    # Parent process reads the message
    os.close(pipe_out)  # Close writing end
    message = os.read(pipe_in, 1024)  # Read data from the pipe
    print(f"Parent: Received from child: {message.decode()}")
    os.close(pipe_in)  # Close reading end

    # Wait for the child to finish
    assistant.join()
    print("Parent: Bakery is closing!")
