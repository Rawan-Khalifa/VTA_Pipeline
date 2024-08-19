import numpy as np
import nibabel as nib

def create_2d_masks(shape=(64, 64)):
    """
    Create two 2D binary masks with one square centered and the second square
    shifted to the left by half the width of the original square.
    
    Parameters:
    shape (tuple): The shape of the 2D mask.
    
    Returns:
    mask1, mask2: Two binary masks.
    """
    mask1 = np.zeros(shape, dtype=np.uint8)
    mask2 = np.zeros(shape, dtype=np.uint8)

    # Define the size of the square regions
    size = 32

    # Create the first square mask (centered)
    start1 = (shape[0] // 2) - (size // 2)
    mask1[start1:start1+size, start1:start1+size] = 1

    # Create the second square mask (shifted to the left by half the width of the square)
    shift = size // 2
    mask2[start1:start1+size, start1-shift:start1-shift+size] = 1

    return mask1, mask2

def calculate_jaccard_index(mask1, mask2):
    """
    Calculate the Jaccard index between two binary masks.
    
    Parameters:
    mask1, mask2: Two binary masks.
    
    Returns:
    jaccard_index (float): The Jaccard index between the two masks.
    """
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    jaccard_index = intersection / union
    return jaccard_index

# Create the 2D masks
mask1, mask2 = create_2d_masks()

# Calculate and print the Jaccard index
jaccard_index = calculate_jaccard_index(mask1, mask2)
print(f"Jaccard Index: {jaccard_index:.2f}")

# Save the masks as NIfTI files
affine = np.eye(4)  # Identity affine, adjust if needed

nifti1 = nib.Nifti1Image(mask1, affine)
nib.save(nifti1, '/Users/rwankhalifa/Downloads/mask1_2d.nii.gz')

nifti2 = nib.Nifti1Image(mask2, affine)
nib.save(nifti2, '/Users/rwankhalifa/Downloads/mask2_2d.nii.gz')

print("2D Masks saved in /Users/rwankhalifa/Downloads as 'mask1_2d.nii.gz' and 'mask2_2d.nii.gz'")
