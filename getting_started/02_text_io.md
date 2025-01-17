# Text input/output

In this section we will explore how to write and/or retrieve our data from
text files.

Most of the functionality for reading/writing files and manipulating strings
is available without any imports. However, you can find some additional
functionality in the
[`string`](https://docs.python.org/3/library/string.html) module.

Most of the string functions are available as methods on string objects. This
means that you can use the ipython autocomplete to check for them.

```
empty_string = ''
```

```
# after running the code block above,
# put your cursor after the dot and
# press tab to get a list of methods
empty_string.
```

* [Reading/writing files](#reading-writing-files)
* [Creating new strings](#creating-new-strings)
  * [String syntax](#string-syntax)
    * [Unicode versus bytes](#unicode-versus-bytes)
  * [Converting objects into strings](#converting-objects-into-strings)
  * [Combining strings](#combining-strings)
  * [String formattings](#string-formatting)
* [Extracting information from strings](#extracting-information-from-strings)
  * [Splitting strings](#splitting-strings)
  * [Converting strings to numbers](#converting-strings-to-numbers)
  * [Regular expressions](#regular-expressions)
* [Exercises](#exercises)

<a class="anchor" id="reading-writing-files"></a>

## Reading/writing files


The syntax to open a file in python is `with open(<filename>, <mode>) as
<file_object>: <block of code>`, where
* `filename` is a string with the name of the file

* `mode` is one of `'r'` (for read-only access), `'w'` (for writing a file,
  this wipes out any existing content), `'a'` (for appending to an existing
  file). A `'b'` can be added to any of these to open the file in "byte"-mode,
  which prevents python from interpreting non-text (e.g., NIFTI) files as text.

* `file_object` is a variable name which will be used within the `block of
  code` to access the opened file.

For example the following will read all the text in `README.md` and print it.
```
with open('README.md', 'r') as readme_file:
    print(readme_file.read())
```

> The `with` statement is an advanced python feature, however you will
> probably only encounter it when opening files. In that context it merely
> ensures that the file will be properly closed as soon as the program leaves
> the `with` statement (even if an error is raised within the `with`
> statement).

You could also use the `readlines()` method to get a list of all the lines, or
simply "loop over" the file object to get the lines one by one:

```
with open('README.md', 'r') as readme_file:
    print('First five lines...')
    for i, line in enumerate(readme_file):
        # each line is returned with its
        # newline character still intact,
        # so we use rstrip() to remove it.
        print(f'{i}: {line.rstrip()}')
        if i == 4:
            break
```

> enumerate takes any sequence and returns 2-element tuples with the index and the sequence item

A very similar syntax is used to write files:
```
with open('02_text_io/my_file', 'w') as my_file:
    my_file.write('This is my first line\n')
    my_file.writelines(['Second line\n', 'and the third\n'])
```

Note that new line characters do not get added automatically. We can investigate
the resulting file using

```
!cat 02_text_io/my_file
```


> In Jupyter notebook, (and in `ipython`/`fslipython`), any lines starting
> with `!` will be interpreted as shell commands. It is great when playing
> around in a Jupyter notebook or in the `ipython` terminal, however it is an
> ipython-only feature and hence is not available when writing python
> scripts. How to call shell commands from python will be discussed in the
> `scripts` practical.

If we want to add to the existing file we can open it in the append mode:
```
with open('02_text_io/my_file', 'a') as my_file:
    my_file.write('More lines is always better\n')
!cat 02_text_io/my_file
```

Below we will discuss how we can convert python objects to strings to store in
these files and how to extract those python objects from strings again.

<a class="anchor" id="creating-new-strings"></a>
## Creating new strings

<a class="anchor" id="string-syntax"></a>
### String syntax


Single-line strings can be created in python using either single or double
quotes:

```
a_string = 'To be or not to be'
same_string = "To be or not to be"
print(a_string == same_string)
```

The main rationale for choosing between single or double quotes, is whether
the string itself will contain any quotes. You can include a single quote in a
string surrounded by single quotes by escaping it with the `\` character,
however in such a case it would be more convenient to use double quotes:

```
a_string = "That's the question"
same_string = 'That\'s the question'
print(a_string == same_string)
```

New-lines (`\n`), tabs (`\t`) and many other special characters are supported
```
a_string = "This is the first line.\nAnd here is the second.\n\tThe third starts with a tab."
print(a_string)
```

You can even include unicode characters:
```
a_string = "Python = 🐍"
print(a_string)
```

However, the easiest way to create multi-line strings is to use a triple quote (again single or double quotes can be used). Triple quotes allow your string to span multiple lines:
```
multi_line_string = """This is the first line.
And here is the second.
\tThird line starts with a tab."""
print(multi_line_string)
```

If you don't want python to reintepret your `\n`, `\t`, etc. in your strings, you can prepend the quotes enclosing the string with an `r`. This will lead to python interpreting the following string as raw text.
```
single_line_string = r"This string is not multiline.\nEven though it contains the \n character"
print(single_line_string)
```

One pitfall when creating a list of strings is that python automatically concatenates string literals, which are only separated by white space:
```
my_list_of_strings = ['a', 'b', 'c' 'd', 'e']
print("The 'c' and 'd' got concatenated, because we forgot the comma:", my_list_of_strings)
```
> This will lead to a syntax warning in python 3.8 or greater

<a class="anchor" id="unicode-versus-bytes"></a>
#### unicode versus bytes

> **Note**: You can safely skip this section if you do not have any plans to
> work with binary files or non-English text in Python, and you do  not want
> to know how to insert poop emojis into your code.


To encourage the spread of python around the world, python 3 switched to using
unicode as the default for strings and code (which is one of the main reasons
for the incompatibility between python 2 and 3).  This means that each element
in a string is a unicode character (using [UTF-8
encoding](https://docs.python.org/3/howto/unicode.html)), which can consist of
one or more bytes.  The advantage is that any unicode characters can now be
used in strings or in the code itself:

```
Δ = "café"
print(Δ)
```


In python 2 each element in a string was a single byte rather than a
potentially multi-byte character. You can convert back to interpreting your
sequence as a unicode string or a byte array using:

* `encode()` called on a string converts it into a bytes array (`bytes` object)
* `decode()` called on a `bytes` array converts it into a unicode string.

```
delta = "Δ"
print('The character', delta, 'consists of the following 2 bytes', delta.encode())
```

These byte arrays can be created directly by prepending the quotes enclosing
the string with a `b`, which tells python 3 to interpret the following as a
byte array:

```
a_byte_array = b'\xce\xa9'
print('The two bytes ', a_byte_array, ' become single unicode character (', a_byte_array.decode(), ') with UTF-8 encoding')
```

Especially in code dealing with strings (e.g., reading/writing of files) many
of the errors arising of running python 2 code in python 3 arise from the
mixing of unicode strings with byte arrays. Decoding and/or encoding some of
these objects can often fix these issues.

By default any file opened in python will be interpreted as unicode. If you
want to treat a file as raw bytes, you have to include a 'b' in the `mode`
when calling the `open()` function:

```
import os.path as op
with open(op.expandvars('${FSLDIR}/data/standard/MNI152_T1_1mm.nii.gz'), 'rb') as gzipped_nifti:
    print('First few bytes of gzipped NIFTI file:', gzipped_nifti.read(10))
```

> We use the `expandvars()` function here to insert the FSLDIR environmental
> variable into our string. This function will be presented in the file
> management practical.


<a class="anchor" id="converting-objects-into-strings"></a>
### Converting objects into strings

There are two functions to convert python objects into strings, `repr()` and
`str()`.  All other functions that rely on string-representations of python
objects will use one of these two (for example the `print()` function will
call `str()` on the object).

The goal of the `str()` function is to be readable, while the goal of `repr()`
is to be unambiguous. Compare

```
print(str("3"))
print(str(3))
```
with

```
print(repr("3"))
print(repr(3))
```
In both cases you get the value of the object (3), but only the `repr` returns enough information to actually know the type of the object.

Perhaps the difference is clearer with a more advanced object.
The `datetime` module contains various classes and functions to work with dates (there is also a `time` module).
Here we will look at the alternative string representations of the `datetime` object itself:
```
from datetime import datetime
print('str(): ', str(datetime.now()))
print('repr(): ', repr(datetime.now()))
```
Note that the result from `str()` is human-readable as a date, while the result from `repr()` is more useful if you wanted to recreate the `datetime` object.

<a class="anchor" id="combining-strings"></a>
### Combining strings
The simplest way to concatenate strings is to simply add them together:
```
a_string = "Part 1"
other_string = "Part 2"
full_string = a_string + ", " + other_string
print(full_string)
```

Given a whole sequence of strings, you can concatenate them together using the `join()` method:
```
list_of_strings = ['first', 'second', 'third', 'fourth']
full_string = ', '.join(list_of_strings)
print(full_string)
```

Note that the string on which the `join()` method is called (`', '` in this case) is used as a delimiter to separate the different strings. If you just want to concatenate the strings you can call `join()` on the empty string:
```
list_of_strings = ['first', 'second', 'third', 'fourth']
full_string = ''.join(list_of_strings)
print(full_string)
```

<a class="anchor" id="string-formatting"></a>
### String formatting
Using the techniques in [Combining strings](#combining-strings) we can build simple strings. For longer strings it is often useful to first write a template strings with some placeholders, where variables are later inserted. Built into python are currently 4 different ways of doing this (with many packages providing similar capabilities):
* [formatted string literals](https://docs.python.org/3/reference/lexical_analysis.html#f-strings) (these are only available in python 3.6+)
* [new-style formatting](https://docs.python.org/3/library/string.html#format-string-syntax).
* printf-like [old-style formatting](https://docs.python.org/3/library/stdtypes.html#old-string-formatting)
* bash-like [template-strings](https://docs.python.org/3/library/string.html#template-strings)

Here we provide a single example using the first three methods, so you can recognize them in the future.

First the old print-f style. Note that this style is invoked by using the modulo (`%`) operator on the string. Every placeholder (starting with the `%`) is then replaced by one of the values provided.
```
a = 3
b = 1 / 3

print('%.3f = %i + %.3f' % (a + b, a, b))
print('%(total).3f = %(a)i + %(b).3f' % {'a': a, 'b': b, 'total': a + b})
```

Then the recommended new style formatting (You can find a nice tutorial [here](https://www.digitalocean.com/community/tutorials/how-to-use-string-formatters-in-python-3)). Note that this style is invoked by calling the `format()` method on the string and the placeholders are marked by the curly braces `{}`.
```
a = 3
b = 1 / 3

print('{:.3f} = {} + {:.3f}'.format(a + b, a, b))
print('{total:.3f} = {a} + {b:.3f}'.format(a=a, b=b, total=a+b))
```
Note that the variable `:` delimiter separates the variable identifiers on the left from the formatting rules on the right.

Finally the new, fancy formatted string literals (only available in python 3.6+).
This new format is very similar to the recommended style, except that all placeholders are automatically evaluated in the local environment at the time the template is defined.
This means that we do not have to explicitly provide the parameters (and we can evaluate the sum inside the string!), although it does mean we also can not re-use the template.
```
a = 3
b = 1/3

print(f'{a + b:.3f} = {a} + {b:.3f}')
```

These f-strings are extremely useful when creating print or error messages for debugging, 
especially with the new support for self-documenting in python 3.8 (see 
[here](https://docs.python.org/3/whatsnew/3.8.html#f-strings-support-for-self-documenting-expressions-and-debugging)):
```
a = 3
b = 1/3

print(f'{a + b=}')
```
Note that this prints both the expression `a + b` and the output (this block will raise an error for python <= 3.7). 


<a class="anchor" id="extracting-information-from-strings"></a>
## Extracting information from strings

The techniques shown in this section are useful if you are loading data from a
small text file or user input, or parsing a small amount of output from
e.g. `fslstats`. However, if you are working with large structured text data
(e.g. a big `csv` file), you should use the I/O capabilities of `numpy` or
`pandas` instead of doing things manually - this is covered in separate
practcals.

<a class="anchor" id="splitting-strings"></a>
### Splitting strings
The simplest way to extract a sub-string is to use slicing (see previous practical for more details):
```
a_string = 'abcdefghijklmnopqrstuvwxyz'
print(a_string[10])  # create a string containing only the 11th character
print(a_string[20:])  # create a string containing the 21st character onward
print(a_string[::-1])  # creating the reverse string
```

If you are not sure, where to cut into a string, you can use the `find()` method to find the first occurrence of a sub-string or `findall()` to find all occurrences.
```
a_string = 'abcdefghijklmnopqrstuvwxyz'
index = a_string.find('fgh')
print(a_string[:index])  # extracts the sub-string up to the first occurence of 'fgh'
print('index for non-existent sub-string', a_string.find('cats'))  # note that find returns -1 when it can not find the sub-string rather than raising an error.
```

You can automate this process of splitting a string at a sub-string using the `split()` method. By default it will split a string at the white space.
```
print('The split() method\trecognizes a wide variety\nof white space'.split())
```

To separate a comma separated list we will need to supply the delimiter to the `split()` method. We can then use the `strip()` method to remove any whitespace at the beginning or end of the string:
```
scientific_packages_string = "numpy, scipy, pandas, matplotlib, nibabel"
list_with_whitespace = scientific_packages_string.split(',')
print(list_with_whitespace)
list_without_whitespace = [individual_string.strip() for individual_string in list_with_whitespace]
print(list_without_whitespace)
```
> We use the syntax `[<expr> for <element> in <sequence>]` here which applies the `expr` to each `element` in the `sequence` and returns the resulting list. This is a list comprehension - a convenient form in python to create a new list from the old one.


<a class="anchor" id="converting-strings-to-numbers"></a>
### Converting strings to numbers


Once you have extracted a number from a string, you can convert it into an
actual integer or float by calling respectively `int()` or `float()` on
it. `float()` understands a wide variety of different ways to write numbers:

```
print(int("3"))
print(float("3"))
print(float("3.213"))
print(float("3.213e5"))
print(float("3.213E-25"))
```


<a class="anchor" id="regular-expressions"></a>
### Regular expressions
Regular expressions are used for looking for specific patterns in a longer string. This can be used to extract specific information from a well-formatted string or to modify a string. In python regular expressions are available in the [re](https://docs.python.org/3/library/re.html#re-syntax) module.

A full discussion of regular expression goes far beyond this practical. If you are interested, have a look [here](https://docs.python.org/3/howto/regex.html).

<a class="anchor" id="exercises"></a>
## Exercises
### Joining/splitting strings
The file 02_text_io/input.txt contains integers in a 2-column format (separated by spaces). Read in this file and write it back out in 2-rows separated by comma's.

```
input_filename = '02_text_io/input.txt'
output_filename = '02_text_io/output.txt'

with open(input_filename, 'r') as input_file:
    ...

with open(output_filename, 'w') as output_file:
    ...
```

### String formatting and regular expressions
Given a template for MRI files:
`s<subject_id>/<modality>_<res>mm.nii.gz`
where `<subject_id>` is a 6-digit subject-id, `<modality>` is one of T1w, T2w, or PD, and `<res>` is the resolution of the image (up to one digits behind the dot, e.g. 1.5)
Write a function that takes the subject_id (as an integer), the modality (as a string), and the resolution (as a float) and returns the complete filename (Hint: use one of the formatting techniques mentioned in [String formatting](#string-formatting)).
```
def get_filename(subject_id, modality, resolution):
    ...
```

For a more difficult exercise, write a function that extracts the subject id, modality, and resolution from a filename name (using a regular expression or by using `find` and `split` to access relevant parts of the string)
```
def get_parameters(filename):
    ...
    return subject_id, modality, resolution
```
