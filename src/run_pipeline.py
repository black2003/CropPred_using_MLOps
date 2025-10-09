"""
Main pipeline runner script
Executes the complete ML pipeline stages in sequence
"""
import subprocess
import sys
import os

def run_pipeline():
    """Run the complete ML pipeline"""
    # Change to parent directory to run from project root
    original_dir = os.getcwd()
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    stages = [
        ("Data Ingestion", "python src/data_ingestion.py"),
        ("Data Preprocessing", "python src/data_preprocessing.py"),
        ("Feature Engineering", "python src/feature_engineering.py"),
        ("Model Training", "python src/model_engineering.py"),
        ("Model Evaluation", "python src/model_evaluation.py")
    ]
    
    try:
        for stage_name, command in stages:
            print(f"\n{'='*50}")
            print(f"Running {stage_name}")
            print(f"{'='*50}")
            
            try:
                result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Warnings:", result.stderr)
            except subprocess.CalledProcessError as e:
                print(f"Error in {stage_name}: {e}")
                print(f"Error output: {e.stderr}")
                sys.exit(1)
        
        print(f"\n{'='*50}")
        print("Pipeline completed successfully!")
        print(f"{'='*50}")
    
    finally:
        # Return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    run_pipeline()