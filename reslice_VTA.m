% Define the base directories
patient_base_dir = '/Volumes/MORRISON/retro_clin/';
atlas_file = '/Users/rkhalifa/Documents/Distal Minimal Atlas/t1.nii';

% Get a list of all patient directories
patient_dirs = dir(fullfile(patient_base_dir, 'PDa*'));

% Initialize cell arrays to track processed and not processed patients
processed_patients = {};
not_processed_patients = {};

% Loop through each patient directory
for i = 1:length(patient_dirs)
    patient_dir = patient_dirs(i).name;
    patient_number_str = patient_dir(4:end);  % Extract the patient number as a string
    patient_number = str2double(patient_number_str);  % Convert to number for further processing
    
    % Determine the two-digit format for the file names
    if patient_number < 100
        file_patient_number = sprintf('%d', patient_number);  % Two-digit format for file names
    else
        file_patient_number = patient_number_str;  % Three-digit format for file names
    end
    
    % Define hemisphere suffixes
    hemispheres = {'L', 'R'};
    
    % Initialize flag to check if any hemisphere is processed
    is_processed = false;
    
    % Loop through each hemisphere
    for j = 1:length(hemispheres)
        hemisphere = hemispheres{j};
        
        % Build the paths to the NIfTI files
        nii_file = fullfile(patient_base_dir, patient_dir, ...
            'derivatives', 'leaddbs', 'sub-leads', 'stimulations', 'MNI152NLin2009bAsym', ...
            ['pd', file_patient_number], ...
            ['sub-leads_sim-binary_model-simbio_hemi-', hemisphere, '.nii']);
        
        % Check if the file exists before processing
        if exist(nii_file, 'file')
            % Load the VTA and MNI files
            VTA = spm_vol(nii_file);
            MNI = spm_vol(atlas_file);
            
            % Reslice the images
            spm_reslice({MNI.fname, VTA.fname}, struct('which', 1, 'interp', 1, 'mask', 0, 'mean', 0));
            
            % Display progress
            disp(['Processed: Patient ', patient_number_str, ', Hemisphere ', hemisphere]);
            
            % Set flag to true as at least one hemisphere was processed
            is_processed = true;
        else
            % Display a message if the file does not exist
            disp(['File not found for Patient ', patient_number_str, ', Hemisphere ', hemisphere]);
        end
    end
    
    % Track the patient based on whether they were processed or not
    if is_processed
        processed_patients{end+1} = patient_number_str;  % Add to processed list
    else
        not_processed_patients{end+1} = patient_number_str;  % Add to not processed list
    end
end

% Display summary of processed and not processed patients
disp('Summary of Processing:');
disp('----------------------');

if ~isempty(processed_patients)
    disp('Patients processed:');
    disp(processed_patients);
else
    disp('No patients were processed.');
end

if ~isempty(not_processed_patients)
    disp('Patients not processed (no valid files found):');
    disp(not_processed_patients);
else
    disp('All patients were processed successfully.');
end
