import asyncio
import httpx
import logging
import time
import requests

url =  "http://localhost:8080/fragment?id={id}"
max_concurrent_workers = 550 # you can state this value with a binary search as well

logging.basicConfig(level=logging.INFO)

def find_top_id():
    low = 1
    high = 10000000000000000000000000 # random high upperbound

    while low <= high:
        mid = (low + high) // 2
        response = requests.get(url.format(id=mid))

        if response.status_code == 200:
            low = mid + 1  # Valid, try higher
        else:
            high = mid - 1  # Invalid, try lower

    return high  # This is the last successful ID

async def get_piece(client, id, pieces, queue):
    try:
        response = await client.get(url.format(id=id))
        if response.status_code == 200:
            piece = response.json()
            piece.pop("id", None)
            await queue.put(piece)
    except httpx.RequestError as e:
        logging.error(f"Request failed for id {id}: {e}")


async def main():
    pieces = []
    tasks = []
    queue = asyncio.Queue()
    i = 0
    start = time.time()
    
    async with httpx.AsyncClient(http2=True) as client:
        while (time.time() - start) < 59:
            while len(tasks) < max_concurrent_workers:
                tasks.append(asyncio.create_task(get_piece(client, i, pieces, queue)))
                i += 1
            await asyncio.gather(*tasks)
            tasks.clear()
    
        for task in tasks:
            task.cancel()

    pieces = []
    while not queue.empty():
        pieces.append(await queue.get())
    queue.task_done()

    sorted_pieces = sorted(pieces, key = lambda x: x['index'])
    return sorted_pieces


if __name__ == '__main__':
    start = time.perf_counter()
    result = asyncio.run(main())
    end = time.perf_counter()
    message = ' '.join(dict.fromkeys(x["text"] for x in result))
    print(f"Retrieved {len(result)} pieces in {end - start:.2f} seconds")
    print(f"message: {message}")

    print("Message has been collected.. Calculating total amount of pieces..")
    start = time.perf_counter()
    total_amount_of_pieces = find_top_id()
    end = time.perf_counter()
    print(f"Retrieved total amout of pieces: {total_amount_of_pieces} in {end - start:.2f} seconds")
    print(f"total amount of pieces is: {total_amount_of_pieces} actually the maximum value for a 64-bit signed integer. =O")