import asyncio
import websockets

async def read_websocket_stream():
    # Replace with your actual WebSocket stream URL
    uri = "ws://localhost:8000/ws"
    
    # Establish a secure context connection
    async with websockets.connect(uri) as websocket:
        print(f"Connected to stream: {uri}")
        
        # Continuously listen and read incoming stream data
        async for message in websocket:
            print(f"Stream data received: {message}")

# Run the asynchronous event loop
if __name__ == "__main__":
    asyncio.run(read_websocket_stream())