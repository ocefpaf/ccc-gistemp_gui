.. Next week is the GSoC mid-term evaluation period.  Please will each
   student write a mid-term blog post:
   
   - summarise your work so far;
   - describe obstacles you have faced and how you have overcome them;
   - say what you are intend to achieve in the remaining time;
   - relate all this to your original project proposal and thus to the
     foundation goals.

   500 to 1000 words, I suppose, by Monday 11th.


Midterm blog post
=================

Hello, my name is Filipe Fernandes and I'm a Google Summer of Code (GSoC)
student for the Climate Code Foundation (CCF).

I've worked mostly on packaging and cross-distribution of ccc-gistemp.

The current ccc-gistemp code is a program for people with at least
intermediate computer skills. It must be run from the a command line
terminal and it
is difficult to make multiple runs and comparisons.

We want to change that, making ccc-gistemp available to a broader
audience.

The progress we have made towards that goal are:

 #. Added a Command Line Interface (CLI) that unify all calls to run/vischeck;
 #. Package ccc-gistemp via a standard Python setup.py;
 #. Registered the code at PyPI;
 #. Implemented py2exe (Windows) and py2app (Mac) for a frozen version of the
    CLI
 #. Started a Graphical User Interface (GUI).


The PyPI package has 63 downloads so far (as of -07-10),
which is quite impressive,
since there was no advertisement. A Linux package was also added to the Open
Build Service (OBS), but the number of downloads is not available.

Via the OBS one can create live CDs with the code or virtual machines that run
on Virtual Box or Amazon EC2 making the code even more accessible.

I decided to tackle the GUI early in the project schedule due to its importance and higher
difficulty (tackle largest risk first). I never used wxPython before,
but I'm glad with the results so far.

The GUI is still under development, but the current version already runs
ccc-gistemp similar to the CLI. We are working in ways to visualize
the results and compare different runs.

The second half of the GSoC period I'll be working with the GUI and
implementing an alternative core to ccc-gistemp using NumPy.

My original proposal has changed a little bit, I'm favoring the GUI instead of
the NumPy implementation. I believe that the foundation of a good user interface
is crucial to achieve the foundation goals.
