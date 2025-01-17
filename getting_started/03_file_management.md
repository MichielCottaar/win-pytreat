# File management


In this section we will introduce you to file management - how do we find and
manage files, directories and paths in Python?


Most of Python's built-in functionality for managing files and paths is spread
across the following modules:


 - [`os`](https://docs.python.org/3/library/os.html)
 - [`shutil`](https://docs.python.org/3/library/shutil.html)
 - [`os.path`](https://docs.python.org/3/library/os.path.html)
 - [`glob`](https://docs.python.org/3/library/glob.html)
 - [`fnmatch`](https://docs.python.org/3/library/fnmatch.html)


The `os` and `shutil` modules have functions allowing you to manage _files and
directories_. The `os.path`, `glob` and `fnmatch` modules have functions for
managing file and directory _paths_.


> Another standard library -
> [`pathlib`](https://docs.python.org/3/library/pathlib.html) - was added in
> Python 3.4, and provides an object-oriented interface to path management. We
> aren't going to cover `pathlib` here, but feel free to take a look at it if
> you are into that sort of thing.


## Contents


If you are impatient, feel free to dive straight in to the exercises, and use the
other sections as a reference. You might miss out on some neat tricks though.


* [Managing files and directories](#managing-files-and-directories)
  * [Querying and changing the current directory](#querying-and-changing-the-current-directory)
  * [Directory listings](#directory-listings)
  * [Creating and removing directories](#creating-and-removing-directories)
  * [Moving and removing files](#moving-and-removing-files)
  * [Walking a directory tree](#walking-a-directory-tree)
  * [Copying, moving, and removing directory trees](#copying-moving-and-removing-directory-trees)
* [Managing file paths](#managing-file-paths)
  * [File and directory tests](#file-and-directory-tests)
  * [Deconstructing paths](#deconstructing-paths)
  * [Absolute and relative paths](#absolute-and-relative-paths)
  * [Wildcard matching a.k.a. globbing](#wildcard-matching-aka-globbing)
  * [Expanding the home directory and environment variables](#expanding-the-home-directory-and-environment-variables)
  * [Cross-platform compatibility](#cross-platform-compatbility)
* [FileTree](#filetree)
* [Exercises](#exercises)
  * [Re-name subject directories](#re-name-subject-directories)
  * [Re-organise a data set](#re-organise-a-data-set)
  * [Solutions](#solutions)
* [Appendix: Exceptions](#appendix-exceptions)



<a class="anchor" id="managing-files-and-directories"></a>
## Managing files and directories


The `os` module contains functions for querying and changing the current
working directory, moving and removing individual files, and for listing,
creating, removing, and traversing directories.


```
import os
import os.path as op
from pathlib import Path
```


> If you are using a library with a long name, you can create an alias for it
> using the `as` keyword, as we have done here for the `os.path` module.


<a class="anchor" id="querying-and-changing-the-current-directory"></a>
### Querying and changing the current directory


You can query and change the current directory with the `os.getcwd` and
`os.chdir` functions.


> Here we're also going to use the `expanduser` function from the `os.path`
> module, which allows us to expand the tilde character to the user's home
> directory This is [covered in more detail
> below](#expanding-the-home-directory-and-environment-variables).


```
cwd = os.getcwd()
print(f'Current directory: {cwd}')

os.chdir(op.expanduser('~'))
print(f'Changed to: {os.getcwd()}')

os.chdir(cwd)
print(f'Changed back to: {cwd}')
```


For the rest of this practical, we're going to use a little data set that has
been pre-generated, and is located in a sub-directory called
`03_file_management`.


```
os.chdir('03_file_management')
```


<a class="anchor" id="directory-listings"></a>
### Directory listings


Use the `os.listdir` function to get a directory listing (a.k.a. the Unix `ls`
command):


```
cwd = os.getcwd()
listing = os.listdir(cwd)
print(f'Directory listing: {cwd}')
print('\n'.join(listing))
print()

datadir = 'raw_mri_data'
listing = os.listdir(datadir)
print(f'Directory listing: {datadir}')
print('\n'.join(listing))
```


> Check out the `os.scandir` function as an alternative to `os.listdir`, if
> you have performance problems on large data sets.


> In the code above, we used the string `join` method to print each path in
> our directory listing on a new line. If you have a list of strings, the
> `join` method is a handy way to insert a delimiting character or string
> (e.g. newline, space, tab, comma - any string you want), between each string
> in the list.


<a class="anchor" id="creating-and-removing-directories"></a>
### Creating and removing directories


You can, not surprisingly, use the `os.mkdir` function to make a
directory. The `os.makedirs` function is also handy - it is equivalent to
`mkdir -p` in Unix:


```
print(os.listdir('.'))
os.mkdir('onedir')
os.makedirs('a/big/tree/of/directories')
print(os.listdir('.'))
```


The `os.rmdir` and `os.removedirs` functions perform the reverse
operations. The `os.removedirs` function will only remove empty directories,
and you must pass it the _leaf_ directory, just like `rmdir -p` in Unix:


```
os.rmdir('onedir')
os.removedirs('a/big/tree/of/directories')
print(os.listdir('.'))
```


<a class="anchor" id="moving-and-removing-files"></a>
### Moving and removing files


The `os.remove` and `os.rename` functions perform the equivalent of the Unix
`rm` and `mv` commands for files. Just like in Unix, if the destination file
you pass to `os.rename` already exists, it will be silently overwritten!


```
with open('file.txt', 'wt') as f:
    f.write('This file contains nothing of interest')

print(os.listdir())
os.rename('file.txt', 'file2.txt')
print(os.listdir())
os.remove('file2.txt')
print(os.listdir())
```


The `os.rename` function will also work on directories, but the `shutil.move`
function (covered below) is more flexible.


<a class="anchor" id="walking-a-directory-tree"></a>
### Walking a directory tree


The `os.walk` function is a useful one to know about. It is a bit fiddly to
use, but it is the best option if you need to traverse a directory tree.  It
will recursively iterate over all of the files in a directory tree - by
default it will traverse the tree in a breadth-first manner.


```
# On each iteration of the loop, we get:
#   - root:  the current directory
#   - dirs:  a list of all sub-directories in the root
#   - files: a list of all files in the root
for root, dirs, files in os.walk('raw_mri_data'):
    print('Current directory: {}'.format(root))
    print('  Sub-directories:')
    print('\n'.join(['    {}'.format(d) for d in dirs]))
    print('  Files:')
    print('\n'.join(['    {}'.format(f) for f in files]))
```


> Note that `os.walk` does not guarantee a specific ordering in the lists of
> files and sub-directories that it returns. However, you can force an
> ordering quite easily - see its
> [documentation](https://docs.python.org/3/library/os.html#os.walk) for
> more details.


If you need to traverse the directory depth-first, you can use the `topdown`
parameter:


```
for root, dirs, files in os.walk('raw_mri_data', topdown=False):
    print('Current directory: {}'.format(root))
    print('  Sub-directories:')
    print('\n'.join(['    {}'.format(d) for d in dirs]))
    print('  Files:')
    print('\n'.join(['    {}'.format(f) for f in files]))
```


> Here we have explicitly named the `topdown` argument when passing it to the
> `os.walk` function. This is referred to as a a _keyword argument_ - unnamed
> arguments are referred to as _positional arguments_. We'll give some more
> examples of positional and keyword arguments below.


<a class="anchor" id="copying-moving-and-removing-directory-trees"></a>
### Copying, moving, and removing directory trees


The `shutil` module contains some higher level functions for copying and
moving files and directories.


```
import shutil
```


The `shutil.copy` and `shutil.move` functions work just like the Unix `cp` and
`mv` commands:


```
# copy the source file to a destination file
src = 'raw_mri_data/subj_1/t1.nii'
shutil.copy(src, 'subj_1_t1.nii')

print(os.listdir('.'))

# copy the source file to a destination directory
os.mkdir('data_backup')
shutil.copy('subj_1_t1.nii', 'data_backup')

print(os.listdir('.'))
print(os.listdir('data_backup'))

# Move the file copy into that destination directory
shutil.move('subj_1_t1.nii', 'data_backup/subj_1_t1_backup.nii')

print(os.listdir('.'))
print(os.listdir('data_backup'))

# Move that destination directory into another directory
os.mkdir('data_backup_backup')
shutil.move('data_backup', 'data_backup_backup')

print(os.listdir('.'))
print(os.listdir('data_backup_backup'))
```


The `shutil.copytree` function allows you to copy entire directory trees - it
is the equivalent of the Unix `cp -r` command. The reverse operation is provided
by the `shutil.rmtree` function:


```
shutil.copytree('raw_mri_data', 'raw_mri_data_backup')
print(os.listdir('.'))
shutil.rmtree('raw_mri_data_backup')
shutil.rmtree('data_backup_backup')
print(os.listdir('.'))
```


<a class="anchor" id="managing-file-paths"></a>
## Managing file paths


The `os.path` module contains functions for creating and manipulating file and
directory paths, such as stripping directory prefixes and suffixes, and
joining directory paths in a cross-platform manner. In this code, we are using
`op` to refer to `os.path` - remember that we [created an alias
earlier](#managing-files-and-directories).


> Note that many of the functions in the `os.path` module do not care if your
> path actually refers to a real file or directory - they are just
> manipulating the path string, and will happily generate invalid or
> non-existent paths for you.


<a class="anchor" id="file-and-directory-tests"></a>
### File and directory tests


If you want to know whether a given path is a file, or a directory, or whether
it exists at all, then the `os.path` module has got your back with its
`isfile`, `isdir`, and `exists` functions. Let's define a silly function which
will tell us what a path is:


```
def whatisit(path, existonly=False):

    print('Does {} exist? {}'.format(path, op.exists(path)))

    if not existonly:
        print('Is {} a file? {}'     .format(path, op.isfile(path)))
        print('Is {} a directory? {}'.format(path, op.isdir( path)))
```


> This is the first time in a while that we have defined our own function,
> [hooray!](https://www.youtube.com/watch?v=zQiibNVIvK4). Here's a quick
> refresher on how to write functions in Python, in case you have forgotten.
>
> First of all, all function definitions in Python begin with the `def`
> keyword:
>
> ```
> def myfunction():
>     function_body
> ```
>
> Just like with other control flow tools, such as `if`, `for`, and `while`
> statements, the body of a function must be indented (with four spaces
> please!).
>
> Python functions can be written to accept any number of arguments:
>
> ```
> def myfunction(arg1, arg2, arg3):
>     function_body
> ```
>
> Arguments can also be given default values:
>
> ```
> def myfunction(arg1, arg2, arg3=False):
>     function_body
> ```
>
> In our `whatisit` function above, we gave the `existonly` argument (which
> controls whether the path is only tested for existence) a default value.
> This makes the `existonly` argument optional - we can call `whatisit` either
> with or without this argument.
>
> To return a value from a function, use the `return` keyword:
>
> ```
> def add(n1, n2):
>     return n1 + n2
> ```
>
> Take a look at the [official Python
> tutorial](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
> for more details on defining your own functions.


Now let's use that function to test some paths. Here we are using the
`op.join` function to construct paths - it is [covered
below](#cross-platform-compatbility):


```
dirname  = op.join('raw_mri_data')
filename = op.join('raw_mri_data', 'subj_1', 't1.nii')
nonexist = op.join('very', 'unlikely', 'to', 'exist')

whatisit(dirname)
whatisit(filename)
whatisit(nonexist)
whatisit(nonexist, existonly=True)
```


<a class="anchor" id="deconstructing-paths"></a>
### Deconstructing paths


If you are only interested in the directory or file component of a path then
the `os.path` module has the `dirname`, `basename`, and `split` functions.


```
path = '/path/to/my/image.nii'

print('Directory name:           {}'.format(op.dirname( path)))
print('Base name:                {}'.format(op.basename(path)))
print('Directory and base names: {}'.format(op.split(   path)))
```


> Note here that `op.split` returns both the directory and base names - remember
> that it is super easy to define a Python function that returns multiple values,
> simply by having it return a tuple. For example, the implementation of
> `op.split` might look something like this:
>
>
> ```
> def mysplit(path):
>     dirname  = op.dirname(path)
>     basename = op.basename(path)
>
>     # It is not necessary to use round brackets here
>     # to denote the tuple - the return values will
>     # be implicitly grouped into a tuple for us.
>     return dirname, basename
> ```
>
>
> When calling a function which returns multiple values, you can _unpack_ those
> values in a single statement like so:
>
>
> ```
> dirname, basename = mysplit(path)
>
> print('Directory name: {}'.format(dirname))
> print('Base name:      {}'.format(basename))
> ```


If you want to extract the prefix or suffix of a file, you can use `splitext`:


```
prefix, suffix = op.splitext('image.nii')

print('Prefix: {}'.format(prefix))
print('Suffix: {}'.format(suffix))
```


> Double-barrelled file suffixes (e.g. `.nii.gz`) are the work of the devil.
> Correct handling of them is an open problem in Computer Science, and is
> considered by many to be unsolvable.  For `imglob`, `imcp`, and `immv`-like
> functionality, check out the `fsl.utils.path` and `fsl.utils.imcp` modules,
> part of the [`fslpy`
> project](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/). If you
> are using `fslpython`, then you already have access to all of the functions
> in `fslpy`.



<a class="anchor" id="absolute-and-relative-paths"></a>
### Absolute and relative paths


The `os.path` module has three useful functions for converting between
absolute and relative paths. The `op.abspath` and `op.relpath` functions will
respectively turn the provided path into an equivalent absolute or relative
path.


```
path = op.abspath('relative/path/to/some/file.txt')

print('Absolutised: {}'.format(path))
print('Relativised: {}'.format(op.relpath(path)))
```


By default, the `op.abspath` and `op.relpath` functions work relative to the
current working directory. The `op.relpath` function allows you to specify a
different directory to work from, and another function - `op.normpath` -
allows you create absolute paths with a different starting
point. `op.normpath` will take care of removing duplicate back-slashes,
and resolving references to `"."` and `".."`:


```
path = 'relative/path/to/some/file.txt'
root = '/vols/Data/'
abspath = op.normpath(op.join(root, path))

print('Absolute path: {}'.format(abspath))
print('Relative path: {}'.format(op.relpath(abspath, root)))
```


<a class="anchor" id="wildcard-matching-aka-globbing"></a>
### Wildcard matching a.k.a. globbing


The `glob` module has a function, also called `glob`, which allows you to find
files, based on unix-style wildcard pattern matching.


```
from glob import glob

root = 'raw_mri_data'

# find all niftis for subject 1
images = glob(op.join(root, 'subj_1', '*.nii*'))

print('Subject #1 images:')
print('\n'.join(['  {}'.format(i) for i in images]))

# find all subject directories
subjdirs = glob(op.join(root, 'subj_*'))

print('Subject directories:')
print('\n'.join(['  {}'.format(d) for d in subjdirs]))
```


As with [`os.walk`](walking-a-directory-tree), the order of the results
returned by `glob` is arbitrary. Unfortunately the undergraduate who
acquired this specific data set did not think to use zero-padded subject IDs
(you'll be pleased to know that this student was immediately kicked out of his
college and banned from ever returning), so we can't simply sort the paths
alphabetically. Instead, let's use some trickery to sort the subject
directories numerically by ID:


Let's define a function which, given a subject directory, returns the numeric
subject ID:


```
def get_subject_id(subjdir):

    # Remove any leading directories (e.g. "raw_mri_data/")
    subjdir = op.basename(subjdir)

    # Split "subj_[id]" into two words
    prefix, sid = subjdir.split('_')

    # return the subject ID as an integer
    return int(sid)
```


This function works like so:


```
print(get_subject_id('raw_mri_data/subj_9'))
```


Now that we have this function, we can sort the directories in one line of
code, via the built-in
[`sorted`](https://docs.python.org/3/library/functions.html#sorted)
function.  The directories will be sorted according to the `key` function that
we specify, which provides a mapping from each directory to a sortable
&quot;key&quot;:


```
subjdirs = sorted(subjdirs, key=get_subject_id)
print('Subject directories, sorted by ID:')
print('\n'.join(['  {}'.format(d) for d in subjdirs]))
```


> Note that in Python, we can pass a function around just like any other
> variable - we passed the `get_subject_id` function as an argument to the
> `sorted` function. This is possible (and normal) because functions are
> [first class citizens](https://en.wikipedia.org/wiki/First-class_citizen) in
> Python!


As of Python 3.5, `glob` also supports recursive pattern matching via the
`recursive` flag. Let's say we want a list of all resting-state scans in our
data set:


```
rscans = glob('raw_mri_data/**/rest.nii.gz', recursive=True)

print('Resting state scans:')
print('\n'.join(rscans))
```


Internally, the `glob` module uses the `fnmatch` module, which implements the
pattern matching logic.

* If you are searching your file system for files and directory, use
  `glob.glob`.

* But if you already have a set of paths, you can use the `fnmatch.fnmatch`
  and `fnmatch.filter` functions to identify which paths match your pattern.


Note that the syntax used by `glob` and `fnmatch` is similar, but __not__
identical to the syntax that you are used to from `bash`. Refer to the
[`fnmatch` module](https://docs.python.org/3/library/fnmatch.html)
documentation for details. If you need more complicated pattern matching, you
can use regular expressions, available via the [`re`
module](https://docs.python.org/3/library/re.html).


For example, let's retrieve all images that are in our data set:


```
allimages = glob(op.join('raw_mri_data', '**', '*.nii*'), recursive=True)
print('All images in experiment:')

# Let's just print the first and last few
print('\n'.join(['  {}'.format(i) for i in allimages[:3]]))
print('  .')
print('  .')
print('  .')
print('\n'.join(['  {}'.format(i) for i in allimages[-3:]]))
```


Now let's reduce that list to only those images which are uncompressed:


```
import fnmatch

# filter a list of images
uncompressed = fnmatch.filter(allimages, '*.nii')
print('All uncompressed images:')
print('\n'.join(['  {}'.format(i) for i in uncompressed]))
```


And further reduce the list by identifying which of these images are T1 scans,
and are from our fictional patient group, made up of subjects 1, 4, 7, 8, and
9:


```
patients = [1, 4, 7, 8, 9]

print('All uncompressed T1 images from patient group:')
for filename in uncompressed:

    fullfile = filename
    dirname, filename = op.split(fullfile)
    subjid = get_subject_id(dirname)

    if subjid in patients and fnmatch.fnmatch(filename, 't1.*'):
        print('  {}'.format(fullfile))
```


<a class="anchor" id="expanding-the-home-directory-and-environment-variables"></a>
### Expanding the home directory and environment variables


You have [already been
introduced](#querying-and-changing-the-current-directory) to the
`op.expanduser` function. Another handy function is the `op.expandvars`
function, which will expand expand any environment variables in a path:


```
print(op.expanduser('~'))
print(op.expandvars('$HOME'))
```


<a class="anchor" id="cross-platform-compatbility"></a>
### Cross-platform compatibility


If you are the type of person who likes running code on both Windows and Unix
machines, you will be delighted to learn that the `os`  module has a couple
of useful attributes:


 - `os.sep` contains the separator character that is used in file paths on
   your platform (i.e. &#47; on Unix, &#92; on Windows).
 - `os.pathsep` contains the separator character that is used when creating
   path lists (e.g. on your `$PATH`  environment variable - &#58; on Unix,
   and &#58; on Windows).


You will also find the `op.join` function handy. Given a set of directory
and/or file names, it will construct a path suited to the platform that you
are running on:


```
path = op.join('home', 'fsluser', '.bash_profile')

# if you are on Unix, you will get 'home/fsluser/.bash_profile'.
# On windows, you will get 'home\\fsluser\\.bash_profile'
print(path)

# Tn create an absolute path from
# the file system root, use os.sep:
print(op.join(op.sep, 'home', 'fsluser', '.bash_profile'))
```

> The `Path` object in the built-in [`pathlib`](https://docs.python.org/3/library/pathlib.html) also has
> excellent cross-platform support. If you write your file management code using this class you are far less likely
> to get errors on Windows.

<a class="anchor" id="filetree"></a>
## FileTree
`fslpy` also contains support for `FileTree` objects (docs are 
[here](https://users.fmrib.ox.ac.uk/~paulmc/fsleyes/fslpy/latest/fsl.utils.filetree.html)). 
These `FileTree` objects provide a simple format to define a whole directory structure with multiple subjects, sessions,
scans, etc. In the `FileTree` format the dataset we have been looking at so far would be described by:
```
tree_text = """
raw_mri_data
    subj_{subject}
        rest.nii.gz
        t1.nii
        t2.nii
        task.nii.gz
"""
```
FileTrees are discussed in more detail in the advanced `fslpy` practical.

<a class="anchor" id="exercises"></a>
## Exercises


<a class="anchor" id="re-name-subject-directories"></a>
### Re-name subject directories


Write a function which can rename the subject directories in `raw_mri_data` so
that the subject IDs are padded with zeros, and thus will be able to be sorted
alphabetically. This function:


  - Should accept the path to the parent directory of the data set
    (`raw_mri_data` in this case).
  - Should be able to handle any number of subjects
    > Hint: `numpy.log10`

  - May assume that the subject directory names follow the pattern
    `subj_[id]`, where `[id]` is the integer subject ID.


<a class="anchor" id="re-organise-a-data-set"></a>
### Re-organise a data set


Write a function which can be used to separate the data for each group
(patients: 1, 4, 7, 8, 9, and controls: 2, 3, 5, 6, 10) into sub-directories
`CON` and `PAT`.

This function should work with any number of groups, and should accept three
parameters:

 - The root directory of the data set (e.g. `raw_mri_data`).
 - A list of strings, the labels for each group.
 - A list of lists, with each list containing the subject IDs for one group.


__Extra exercises:__ If you are looking for something more to do, you can find
some more exercises in the file `03_file_management_extra.md`.


<a class="anchor" id="solutions"></a>
### Solutions


Use the `print_solution` function, defined below, to print the solution for a
specific exercise.


```
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import IPython

# Pass the title of the exercise you
# are interested to this function
def print_solution(extitle):
    solfile = ''.join([c.lower() if c.isalnum() else '_' for c in extitle])
    solfile = op.join('.solutions', '{}.py'.format(solfile))

    if not op.exists(solfile):
        print('Can\'t find solution to exercise "{}"'.format(extitle))
        return

    with open(solfile, 'rt') as f:
        code = f.read()

    formatter = HtmlFormatter()
    return IPython.display.HTML('<style type="text/css">{}</style>{}'.format(
        formatter.get_style_defs('.highlight'),
        highlight(code, PythonLexer(), formatter)))
```


<a class="anchor" id="appendix-exceptions"></a>
## Appendix: Exceptions


At some point in your life, a piece of code that you write is inevitably going
to fail, and you are going to have to deal with it. This is particularly
relevant to file management tasks - many of the functions that have been
introduced in this practical can fail for all kinds of reasons, such as
incorrect permissions or ownership, lack of disk space, or a network file
system going down.


Any statement in Python can potentially result in an error. When a line of
code triggers an error, we say that it _raises_ the error (a.k.a. _throws_ in
other languages). When an error occurs, an `Exception` object is raised,
causing execution to stop at the line that caused the error:


```
a = [1, 2, 3]
a.remove(4)
```


The word `Exception` is used instead of `Error` because not all exceptions are
errors. For example, when you type CTRL+C into a running Python program, a
`KeyboardInterrupt` exception will be raised.


> There are many different types of exceptions in Python - a list of all the
> built-in ones can be found
> [here](https://docs.python.org/3/library/exceptions.html). It is also easy
> to define your own exceptions by creating a sub-class of `Exception` (beyond
> the scope of this practical).


Fortunately Python gives us the capability to _catch_ exceptions when they are
raised, using the `try` and `except` keywords. As an example, let's say that
the user asked our program to create a directory somewhere on the file system.
A real program would need to handle situations in which that directory cannot
be created - we might do it like this in Python:


```
import os

dirpath = '/sbin/foo'

try:
    os.mkdir(dirpath)

except OSError as e:
    print('Could not create {}! Reason: {}'.format(dirpath, e))
```


In this example, we have put the `os.mkdir` call inside a `try:` block. Now,
if it raises an `Exception` of type `OSError`, that `OSError` will be _caught_
and passed to the `except:` block. A `try` block must always followed by an
`except` block (and/or a `finally` block - keep reading).


The `except OSError as e:` line means: _if any code in the `try` block raises
an `Exception` of type `OSError`, then catch it, assign it to a variable
called `e`, and pass it to the code inside the `except` block._


### Catching different types of exceptions


It is common for a piece of code to have the potential to raise different
types of exceptions. Python allows you to have multiple `except` blocks
associated with a single `try` block, so you can handle different types of
exceptions in different ways. For example, you might want to print a useful
error message so the user knows what has gone wrong:


```
numerator   = '123'
denominator = 0

try:
    numerator = float(numerator)
    print(numerator / denominator)

except TypeError as e:
    print('Numerator and/or denominator are of the wrong type!')
    print('  ', e)

except ValueError as e:
    print('Numerator is not a float!')
    print('  ', e)

# Note that specifying a variable to refer
# to the Exception object is optional.
except ZeroDivisionError:
    print('Denominator is zero!')
```


Experiment with the above code block - try out different values for the
`numerator` and `denominator`, and see what happens.


You can also specify different types of exceptions in a single `except`
statement:


```
numerator   = '123'
denominator = 0
try:
    numerator = float(numerator)
    print(numerator / denominator)

except (TypeError, ZeroDivisionError) as e:
    print('Numerator and/or denominator are of the '
          'wrong type, or the denominator is zero!')
    print('  ', e)
```


### The catch-all approach


Instead of specifying all of the different types of exceptions that could
occur, it is possible to simply use a single `except` block to catch all
exceptions of type `Exception`:


```
numerator   = 'abc'
denominator = 1

try:
    numerator = float(numerator)
    print(numerator / denominator)

except Exception as e:
    print('Something is wrong with numerator or denominator!')
    print('  ', e)

```


It is generally better practice to be as specific as possible when you are
catching exceptions, but sometimes all you care about is whether your code
worked or didn't, and in this case the you can simply use this catch-all
approach.


__Warning:__ Even though it is possible to, you should __never__ write a
`try`-`except` block like this:


```
try:
    # do stuff
    pass

except:
    # handle exceptions
    pass
```


You don't actually have to specify any exception type in an `except`
statement.  But you should never do this!  As we have already mentioned, not
all exceptions are errors. The above code will catch _all_ exceptions, even
those which do not inherit from the standard `Exception` class. This includes
important exceptions such as `KeyboardInterrupt` and `SystemExit`, which
control important aspects of your program's behaviour.


So you should always, at the very least, specify the `Exception` type:


```
try:
    # do stuff
    pass

except Exception:
    # handle exceptions
    pass
```


### The `finally` keyword


Sometimes, when you are performing a task, you might have some clean-up logic
that must be executed regardless of whether the task succeeded or failed. The
canonical example here is that if you open a file, you must make sure that to
close it when you are finished, otherwise its contents may be corrupted.


```
f = open('raw_mri_data/subj_1/t1.nii', 'rb')
try:
    f.write('ho hum')

except IOError as e:
    print('Error occurred!: ', e)
finally:
    print('Closing file')
    f.close()
```


It is possible to use `try` and `finally` without an `except` block. This is
useful if you have some code that needs some clean-up logic, but you don't
actually want to catch the exception - sometimes it is better for a program
to crash, rather than for errors to be silently suppressed, because it can
be easier to figure out what went wrong:


```
f = open('raw_mri_data/subj_1/t1.nii', 'rb')

try:
    f.write('ho hum')

finally:
    print('Closing file')
    f.close()
```


> The above was just an example - it is generally better practice to use the
> `with` statement when opening files.


You can read more about handling exceptions in Python
[here](https://docs.python.org/3/tutorial/errors.html).


### Raising exceptions


It is possible to generate your own exception at any point by using the
`raise` keyword, and passing it an `Exception` object:


```
raise Exception('Kaboom!')
```


This can be useful if your code detects that something has gone wrong, and
needs to abort.


You can also raise an existing `Exception` from within an `except` block:


```
try:
    print(1 / 0)

except Exception:
    print('Some error occurred!')
    raise
```

This can be useful if you want to print a message when an exception occurs,
but also allow the execption to be propagated upwards.
