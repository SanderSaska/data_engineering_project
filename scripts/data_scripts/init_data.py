import subprocess
import os
import datetime


# Set up logging directory
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
os.makedirs(log_dir, exist_ok=True)

# Create log file for this script
init_log_file = os.path.join(log_dir, 'init_data.log')

def log_message(message):
    """Log a message to the init_data log file."""
    with open(init_log_file, 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - {message}\n")
    print(message)

def run_script(script_path, *args):
    """Run a script and log its output to a file."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    script_name = os.path.basename(script_path).replace('.py', '')
    log_file_path = os.path.join(log_dir, f"{script_name}_{timestamp}.log")
    
    try:
        command = ['python', script_path] + list(args)
        log_message(f"Running command: {' '.join(command)}")
        
        with open(log_file_path, 'w') as log_file:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            log_file.write(result.stdout)
            log_file.write(result.stderr)
        
        log_message(f"Script {script_path} completed successfully. Logs saved at {log_file_path}.")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        with open(log_file_path, 'w') as log_file:
            log_file.write(e.stderr)
        log_message(f"Error running script {script_path}. Check logs at {log_file_path}.")
        raise

def main():
    # Paths to scripts
    api_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../api')
    ingestion_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../ingestion_scripts')

    try:
        log_message("==== Step 1: Running geo_api.py ====")#werks
        geo_data_path = run_script(os.path.join(api_folder, 'geo_api.py'))
        
        log_message("==== Step 2: Running geo_ingest.py ====")#werks
        run_script(os.path.join(ingestion_folder, 'geo_ingest.py'), geo_data_path)
        
        
        log_message("==== Step 3: Running erviss_api.py ====")#werks
        run_script(os.path.join(api_folder, 'erviss_api.py'))
        
        log_message("==== Step 4: Running erviss_ingest.py ====")#werks
        run_script(os.path.join(ingestion_folder, 'erviss_ingest.py'))
        
        log_message("==== Step 5: Running OpenMeteo.py ====")#werks
        run_script(os.path.join(api_folder, 'OpenMeteo.py'))



        log_message("==== Step 6: Running weather_ingest.py ====")#werks

        run_script(os.path.join(ingestion_folder, 'weather_ingest.py'))


            
        log_message("==== Step 7: Running EEA_api.py ====")#works
        run_script(os.path.join(api_folder, 'EEA_api.py'))

        
        log_message("==== Step 8: Running EEA_ingest.py ====")#works

        run_script(os.path.join(ingestion_folder, 'EEA_ingest.py'))

        
        log_message("==== Step 9: Running fill_calendar.py ====")

        run_script(os.path.join(ingestion_folder, 'fill_calendar.py'))
                
        log_message("==== Init data process completed successfully ====")
    except Exception as e:
        log_message(f"An error occurred during the init data process: {e}")

if __name__ == "__main__":
    main()
