import os
import nibabel as nib
import numpy as np
import csv

def load_nifti(file_path):
    """Load a NIfTI file and return the data array."""
    nifti_data = nib.load(file_path)
    return nifti_data.get_fdata()

def binarize_mask(mask):
    """Convert the NIfTI data to a binary mask."""
    binary_mask = np.where(mask > 0, 1, 0)
    return binary_mask

def jaccard_index(mask1, mask2):
    """Calculate the Jaccard Index between two binary masks."""
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    jaccard = intersection.sum() / union.sum()
    return jaccard

def process_hemisphere(stim_file_path, base_dir, hemisphere):
    """Process the Jaccard index calculation for a specific hemisphere."""
    atlas_dir = os.path.join(base_dir, 'Documents/Distal Minimal Atlas', hemisphere)
    stn_file = os.path.join(atlas_dir, 're_STN.nii')
    gpi_file = os.path.join(atlas_dir, 're_GPI.nii')

    # Load and binarize the stimulation and atlas files
    stim_mask = binarize_mask(load_nifti(stim_file_path))
    stn_mask = binarize_mask(load_nifti(stn_file))
    gpi_mask = binarize_mask(load_nifti(gpi_file))

    # Calculate Jaccard Index
    jaccard_stn = jaccard_index(stim_mask, stn_mask)
    jaccard_gpi = jaccard_index(stim_mask, gpi_mask)

    return {'STN': jaccard_stn, 'GPI': jaccard_gpi}

def process_patient(patient_number):
    """Process the Jaccard index calculation for a specific patient."""
    base_dir = '/Volumes/MORRISON/retro_clin'

    # Format patient_number to ensure correct directory and file paths
    patient_dir = f'PDa{int(patient_number):03d}'  # Format to three digits for directory
    file_patient_number = str(int(patient_number))  # Remove leading zeros for file names
    
    # Paths for stimulation files for both hemispheres
    stim_file_paths = {
        'right': f'{base_dir}/{patient_dir}/derivatives/leaddbs/sub-leads/stimulations/MNI152NLin2009bAsym/pd{file_patient_number}/rsub-leads_sim-binary_model-simbio_hemi-R.nii',
        'left': f'{base_dir}/{patient_dir}/derivatives/leaddbs/sub-leads/stimulations/MNI152NLin2009bAsym/pd{file_patient_number}/rsub-leads_sim-binary_model-simbio_hemi-L.nii'
    }
    
    results = {}

    # Process each hemisphere if the file exists
    for side, stim_file_path in stim_file_paths.items():
        if os.path.exists(stim_file_path):
            hemisphere = 'rh' if side == 'right' else 'lh'
            results[side] = process_hemisphere(stim_file_path, '/Users/rwankhalifa', hemisphere)
    
    return results

def save_results_to_csv(all_results, output_file):
    """Save the Jaccard Index results to a CSV file."""
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(["Patient Number", "Left STN Jaccard Index", "Right STN Jaccard Index", "Left GPI Jaccard Index", "Right GPI Jaccard Index"])
        
        for patient_number, hemispheres in all_results.items():
            left_stn = hemispheres.get('left', {}).get('STN', 'N/A')
            right_stn = hemispheres.get('right', {}).get('STN', 'N/A')
            left_gpi = hemispheres.get('left', {}).get('GPI', 'N/A')
            right_gpi = hemispheres.get('right', {}).get('GPI', 'N/A')
            writer.writerow([patient_number, left_stn, right_stn, left_gpi, right_gpi])

def process_all_patients(base_dir, output_file):
    """Process all patients within the specified base directory and save results to CSV."""
    patient_base_dir = os.path.join(base_dir, 'PDa')
    patients = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('PDa')]
    
    all_results = {}
    
    for patient in patients:
        patient_number = patient[3:]  # Extract patient number from directory name

        # Skip non-numeric patient identifiers
        if not patient_number.isdigit():
            print(f"Skipping non-numeric patient identifier: {patient}")
            continue
        
        print(f"Processing patient {patient_number}...")
        results = process_patient(patient_number)
        all_results[patient_number] = results
        
        if 'right' in results:
            print(f"Right Hemisphere - Jaccard Index for STN: {results['right']['STN']}")
            print(f"Right Hemisphere - Jaccard Index for GPI: {results['right']['GPI']}")
    
        if 'left' in results:
            print(f"Left Hemisphere - Jaccard Index for STN: {results['left']['STN']}")
            print(f"Left Hemisphere - Jaccard Index for GPI: {results['left']['GPI']}")
    
    # Save all results to a CSV file
    save_results_to_csv(all_results, output_file)

# Example usage to process all patients and save results
base_dir = '/Volumes/MORRISON/retro_clin'
output_file = '/Users/rwankhalifa/Documents/jaccard_results.csv'

# Process all patients and save results
process_all_patients(base_dir, output_file)

# Check if the CSV file was created correctly
import pandas as pd
df = pd.read_csv(output_file)
df.head()
