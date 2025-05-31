from schubertpy.grassmannian import *
from schubertpy.isotropic_grassmannian import *
from schubertpy.orthogonal_grassmannian import *
import sympy as sp
import csv
import unittest
import time
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from schubertpy.csv_bijection import check_bijection_with_permutation as isbijection
from schubertpy.utils.const import encode


# Dispatcher to map the command to the appropriate function
def dispatch(command, params):
    if command == "OG":
        return OrthogonalGrassmannian(*params)
    elif command == "IG":
        return IsotropicGrassmannian(*params)
    elif command == "Gr":
        return Grassmannian(*params)
    else:
        print(f"Unknown command: {command}")

def process_batch(batch_data, batch_id, test_method='qmult'):
    """Process a batch of test cases"""
    results = []
    batch_start_time = time.time()
    
    print(f"Thread {batch_id}: Starting batch with {len(batch_data)} test cases")
    
    for i, row in enumerate(batch_data):
        try:
            command_with_params = row[0].split('(')
            command = command_with_params[0]
            params = command_with_params[1][:-1]
            params = params.split(',')
            params = [int(p) for p in params]
            
            # Skip non-Gr commands for test_method='qmult_rh'
            if test_method == 'qmult_rh' and command != "Gr":
                continue
            
            gr = dispatch(command, params)
            
            s1 = row[2]
            s2 = row[3]
            
            start = time.time()
            
            if test_method == 'qmult':
                result = gr.qmult(s1, s2)
            elif test_method == 'qmult_rh':
                result = gr.qmult_rh(s1, s2)
            else:
                raise ValueError(f"Unknown test method: {test_method}")
            
            elapsed_time = time.time() - start
            
            result = sp.expand(result.expr).simplify()
            
            expected_result = sp.parse_expr(encode(row[4].replace('^', '**')))
            expected_result = sp.expand(expected_result).simplify()
            
            # Check if results match
            if result == expected_result:
                results.append({
                    'success': True,
                    'row': row,
                    'elapsed_time': elapsed_time,
                    'thread_id': batch_id
                })
                if (i + 1) % 100 == 0:
                    print(f"Thread {batch_id}: Processed {i + 1}/{len(batch_data)} cases")
            else:
                results.append({
                    'success': False,
                    'row': row,
                    'elapsed_time': elapsed_time,
                    'thread_id': batch_id,
                    'error': f"Result mismatch: got {result}, expected {expected_result}"
                })
                
        except Exception as e:
            results.append({
                'success': False,
                'row': row,
                'elapsed_time': 0,
                'thread_id': batch_id,
                'error': str(e)
            })
    
    batch_elapsed_time = time.time() - batch_start_time
    print(f"Thread {batch_id}: Completed batch in {batch_elapsed_time:.2f} seconds")
    
    return results

def load_csv_data(csv_file_path, max_rows=None):
    """Load CSV data into memory"""
    data = []
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for i, row in enumerate(csv_reader):
            if max_rows and i >= max_rows:
                break
            data.append(row)
    return data

def split_into_batches(data, batch_size=1000):
    """Split data into batches"""
    batches = []
    for i in range(0, len(data), batch_size):
        batches.append(data[i:i + batch_size])
    return batches

class TestWithCSVFileThreaded(unittest.TestCase):

    def test_1_threaded(self):
        """Test qmult method with threading"""
        csv_file_path = './schubertpy/testcases/results.csv'
        batch_size = 1000
        max_threads = 7
        
        print("Loading CSV data...")
        all_data = load_csv_data(csv_file_path)
        total_rows = len(all_data)
        print(f"Loaded {total_rows} test cases")
        
        print("Splitting into batches...")
        batches = split_into_batches(all_data, batch_size)
        total_batches = len(batches)
        print(f"Created {total_batches} batches")
        
        # Limit to max_threads batches for this test
        test_batches = batches[:max_threads] if len(batches) > max_threads else batches
        
        print(f"Running {len(test_batches)} batches on {min(max_threads, len(test_batches))} threads...")
        
        start_time = time.time()
        all_results = []
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Submit all batches
            future_to_batch = {
                executor.submit(process_batch, batch, i, 'qmult'): i 
                for i, batch in enumerate(test_batches)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_batch):
                batch_id = future_to_batch[future]
                try:
                    batch_results = future.result()
                    all_results.extend(batch_results)
                except Exception as exc:
                    print(f'Batch {batch_id} generated an exception: {exc}')
        
        total_elapsed = time.time() - start_time
        
        # Analyze results
        successful = sum(1 for r in all_results if r['success'])
        failed = sum(1 for r in all_results if not r['success'])
        total_test_time = sum(r['elapsed_time'] for r in all_results)
        
        print(f"\n=== Test Results ===")
        print(f"Total time: {total_elapsed:.2f} seconds")
        print(f"Total test execution time: {total_test_time:.2f} seconds")
        print(f"Speedup factor: {total_test_time/total_elapsed:.2f}x")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total processed: {len(all_results)}")
        
        # Print any failures
        failures = [r for r in all_results if not r['success']]
        if failures:
            print(f"\n=== Failures ===")
            for failure in failures[:10]:  # Show first 10 failures
                print(f"Thread {failure['thread_id']}: {failure['row']} - {failure['error']}")
        
        # Assert all tests passed
        self.assertEqual(failed, 0, f"{failed} test cases failed")

    def test_2_threaded(self):
        """Test qmult_rh method with threading (Grassmannian only)"""
        csv_file_path = './schubertpy/testcases/results.csv'
        batch_size = 1000
        max_threads = 7
        
        print("Loading CSV data...")
        all_data = load_csv_data(csv_file_path)
        
        # Filter for Grassmannian only
        gr_data = []
        for row in all_data:
            command_with_params = row[0].split('(')
            command = command_with_params[0]
            if command == "Gr":
                gr_data.append(row)
        
        total_rows = len(gr_data)
        print(f"Loaded {total_rows} Grassmannian test cases")
        
        print("Splitting into batches...")
        batches = split_into_batches(gr_data, batch_size)
        total_batches = len(batches)
        print(f"Created {total_batches} batches")
        
        # Limit to max_threads batches for this test
        test_batches = batches[:max_threads] if len(batches) > max_threads else batches
        
        print(f"Running {len(test_batches)} batches on {min(max_threads, len(test_batches))} threads...")
        
        start_time = time.time()
        all_results = []
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            # Submit all batches
            future_to_batch = {
                executor.submit(process_batch, batch, i, 'qmult_rh'): i 
                for i, batch in enumerate(test_batches)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_batch):
                batch_id = future_to_batch[future]
                try:
                    batch_results = future.result()
                    all_results.extend(batch_results)
                except Exception as exc:
                    print(f'Batch {batch_id} generated an exception: {exc}')
        
        total_elapsed = time.time() - start_time
        
        # Analyze results
        successful = sum(1 for r in all_results if r['success'])
        failed = sum(1 for r in all_results if not r['success'])
        total_test_time = sum(r['elapsed_time'] for r in all_results)
        
        print(f"\n=== Test Results ===")
        print(f"Total time: {total_elapsed:.2f} seconds")
        print(f"Total test execution time: {total_test_time:.2f} seconds")
        print(f"Speedup factor: {total_test_time/total_elapsed:.2f}x")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total processed: {len(all_results)}")
        
        # Print any failures
        failures = [r for r in all_results if not r['success']]
        if failures:
            print(f"\n=== Failures ===")
            for failure in failures[:10]:  # Show first 10 failures
                print(f"Thread {failure['thread_id']}: {failure['row']} - {failure['error']}")
        
        # Assert all tests passed
        self.assertEqual(failed, 0, f"{failed} test cases failed")


if __name__ == '__main__':
    unittest.main() 