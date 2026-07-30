Custom node.  saves sampler seeds to ComfyUI Output folder either in a text file or a log file.
I text is selected, there is a seperate file for each seed.  If log file is chosen each seed is wriiten sequentially in the same file.
the log file is handy if you queue up jobs.
Set Up:  Drag a noodle from the node output to the seed line of your sampler node.
If using an old Comfy version, you might have to right click on the sampler node and add a widget to create a seed input.
- Barry Buehler June 24 2026