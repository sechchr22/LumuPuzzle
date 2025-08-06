# 🧩 Puzzle Challenge

Solve the puzzle — fast and efficiently.
---

## 🚀 How to Run

1. **Clone this repo** to your local environment.
2. **Start the puzzle server** using Docker:
   ```bash
   docker run -p 8080:8080 ifajardov/puzzle-server
2. Activate a venv
   ```bash
   python3 -m venv env && source env/bin/activate
3. Install the only dependency: 
    ```bash
    pip install httpx
4. RUN command:
    ```bash
    python3 puzzle.py

## 📌 Strategy Overview
    1. 🔍 Determine Total Number of Pieces
        This was done implementing a binary search that has a time complexity of O(log n) so for this case as big as the quantity of pieces was, we just had to do 64 requests in total to find the total amount of pieces. The criteria for the binary search was that we know we would receive a succesfull 200 response till the limit returned a 400 as status code.

    2. 🧠 Dealing With Astronomical Limits
        The amount of pieces was 9.22 quintillons, That’s more than the number of grains of sand on Earth: This is an unreal number to hit, even more adding that each request would take 200 ms in average so this wouldnt be a real woarkload.
        
        What i can do instead is to propose a solution to get as many pieces the resources i have are capable to get under a min and then get the ordered message from it.

    3. ⚙️ Efficient Parallel Solution
        I already knew i was going to send my batches of requests in parallel but there was a few of conditionals in order to know how to do it efficiently and without breaking the pieces service.

        🛠 Define service capacity: How many requests can we fire in parallel without overload?
        I took a mix between a binary search and manually approach just modifiying the max_concurrent_workers and checking the "sweet spot" however i could have done it with a function implementing binary search as i did to find the total amount of pieces.

        👥 Once worker count is set, i can send batches respecting this concurrency limits.
        As each request completes, i would free up the slot and dispatch a new one — maintaining throughput.

    4. 🧹 Clean & Sort
        The solution then comes down to:
            In a frame of 60 secs i will be sending a batch of requests and inmediatly one of them finishes i would clean them up from the batch so i could be adding more, of course respecting the batching limit. 
            
            Once having the pieces i would just order them with the sorted function that offer a O(n log n) time complexity making it efficient for large unsorted datasets - After it the final action to do is just extract the clean message removing the duplicates. 