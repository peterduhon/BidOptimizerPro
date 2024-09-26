# main.py
import logging
from simulation import run_sequential_bids, run_parallel_bids
from visualization import plot_performance

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    advertisers = ['A', 'B', 'C', 'D', 'E']
    
    # Run sequential bids
    seq_bids, seq_time = run_sequential_bids(advertisers)
    
    # Run parallel bids
    par_bids, par_time = run_parallel_bids(advertisers, max_workers=5)
    
    # Print execution times
    print(f"Sequential execution time: {seq_time:.2f} seconds")
    print(f"Parallel execution time: {par_time:.2f} seconds")
    
    # Plot performance
    plot_performance(seq_time, par_time)

if __name__ == "__main__":
    main()
