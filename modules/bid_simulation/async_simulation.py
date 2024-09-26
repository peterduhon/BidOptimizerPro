# async_simulation.py
import asyncio
import random
import time
import matplotlib.pyplot as plt

async def simulate_bid(advertiser):
    """Asynchronously simulate network latency and generate a random bid amount."""
    latency = random.uniform(0.1, 0.5)
    await asyncio.sleep(latency)  # Simulate network latency
    bid_amount = random.uniform(1, 10)  # Return a random bid amount
    return bid_amount

async def run_sequential_bids(advertisers):
    """Run bids sequentially using asyncio."""
    start_time = time.time()
    bids = []
    for adv in advertisers:
        bid = await simulate_bid(adv)
        bids.append(bid)
    execution_time = time.time() - start_time
    return bids, execution_time

async def run_parallel_bids(advertisers):
    """Run bids in parallel using asyncio.gather."""
    start_time = time.time()
    bids = await asyncio.gather(*(simulate_bid(adv) for adv in advertisers))
    execution_time = time.time() - start_time
    return bids, execution_time

def plot_performance(sequential_time, parallel_time):
    """Plot the execution time comparison."""
    times = [sequential_time, parallel_time]
    labels = ['Sequential', 'Parallel']
    
    plt.bar(labels, times, color=['blue', 'orange'])
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performance Comparison: Sequential vs. Parallel Processing')
    plt.show()

def main():
    advertisers = ['A', 'B', 'C', 'D', 'E']
    
    # Run the event loop
    loop = asyncio.get_event_loop()
    
    # Run sequential bids
    seq_bids, seq_time = loop.run_until_complete(run_sequential_bids(advertisers))
    
    # Run parallel bids
    par_bids, par_time = loop.run_until_complete(run_parallel_bids(advertisers))
    
    # Print execution times
    print(f"Sequential execution time: {seq_time:.2f} seconds")
    print(f"Parallel execution time: {par_time:.2f} seconds")
    
    # Plot performance
    plot_performance(seq_time, par_time)

if __name__ == "__main__":
    main()
