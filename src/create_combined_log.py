import os
import glob
from datetime import datetime

def create_combined_log():
    """
    Creates a combined log file from the most recent stock prices and outstanding shares logs.
    This is called by the batch file after both scripts have run.
    """
    print("Creating combined log file...")
    
    # Find the most recent log files
    stock_logs = glob.glob("stock_prices_log_*.txt")
    shares_logs = glob.glob("outstanding_shares_log_*.txt")
    
    if not stock_logs or not shares_logs:
        print("Could not find both log files to combine")
        return
    
    # Get the most recent files
    latest_stock_log = max(stock_logs, key=os.path.getctime)
    latest_shares_log = max(shares_logs, key=os.path.getctime)
    
    # Create combined log filename
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    combined_log_filename = f"combined_extraction_log_{current_time}.txt"
    
    try:
        with open(combined_log_filename, 'w', encoding='utf-8') as combined_file:
            combined_file.write("COMBINED STOCK PRICES & OUTSTANDING SHARES EXTRACTION LOG\n")
            combined_file.write("=" * 70 + "\n")
            combined_file.write(f"Combined Log Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            combined_file.write(f"Batch File: run_updater_with_shares.bat\n\n")
            
            # Read and include stock prices log
            combined_file.write("STOCK PRICES LOG:\n")
            combined_file.write("-" * 20 + "\n")
            try:
                with open(latest_stock_log, 'r', encoding='utf-8') as stock_file:
                    stock_content = stock_file.read()
                    # Skip the header line and add the content
                    lines = stock_content.split('\n')[4:]  # Skip first 4 header lines
                    combined_file.write('\n'.join(lines))
            except Exception as e:
                combined_file.write(f"Error reading stock prices log: {e}\n")
            
            combined_file.write("\n\n")
            
            # Read and include outstanding shares log
            combined_file.write("OUTSTANDING SHARES LOG:\n")
            combined_file.write("-" * 25 + "\n")
            try:
                with open(latest_shares_log, 'r', encoding='utf-8') as shares_file:
                    shares_content = shares_file.read()
                    # Skip the header line and add the content
                    lines = shares_content.split('\n')[4:]  # Skip first 4 header lines
                    combined_file.write('\n'.join(lines))
            except Exception as e:
                combined_file.write(f"Error reading outstanding shares log: {e}\n")
            
        print(f"Combined log file created: {combined_log_filename}")
        
        # Optionally delete the individual log files
        try:
            os.remove(latest_stock_log)
            os.remove(latest_shares_log)
            print("Cleaned up individual log files")
        except Exception as e:
            print(f"Could not clean up individual log files: {e}")
            
    except Exception as e:
        print(f"Error creating combined log file: {e}")

if __name__ == "__main__":
    create_combined_log() 