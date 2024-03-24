import asyncio
import time

# Synchronous function
def stream():
    for i in range(5):
        # Simulate reading a chunk of data
        time.sleep(1)
        print(f"Stream: Read chunk {i+1}")
    print("Stream: All chunks read")

# Asynchronous function
async def astream():
    for i in range(5):
        # Simulate reading a chunk of data asynchronously
        await asyncio.sleep(1)
        print(f"AStream: Read chunk {i+1}")
    print("AStream: All chunks read")

async def main():
    print("Starting synchronous stream:")
    stream()
    
    # Run astream as a task concurrently
    astream_task = asyncio.create_task(astream())
    print("Starting asynchronous astream concurrently with other tasks:")
    
    # Here you can do other tasks while astream is running
    for i in range(3):
        print(f"Main: Doing other task {i+1}")
        await asyncio.sleep(0.5)
    
    # Wait for astream to finish
    await astream_task

# Run the main function
asyncio.run(main())

