#!/usr/bin/env fslpython

# That first line up there ensures that your
# script will be executed in the fslpython
# environment. If you are writing a general
# Python script, you should use this line
# instead: #!/usr/bin/env python

# In Python, we need to "import" libraries
# (called modules) before we can use them.
import sys
import nibabel as nib

# We can get to our command
# line arguments via sys.argv
fpath = sys.argv[1]

# We can use nibabel to load
# NIFTI images (and other
# neuroimaging data formats)
img = nib.load(fpath)
data = img.get_data()

# Now we're working with a
# numpy array.
nzmean = data[data != 0].mean()

print('mean:', nzmean)
