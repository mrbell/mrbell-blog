Title: Spell checking an IPython notebook
Date: 2015-02-01
Tags: python, how-to
Slug: ipynb-spellchecking

I've been using [IPython notebooks](http://ipython.org/notebook.html) a lot lately for both my personal and professional
research and analysis projects. It's a great tool for keeping code, visualization and analysis together in one place.
It's also convenient for communicating results. Just export your notebook to HTML and it's ready to distribute... except
for the fact that without a spell checker I tend to have a lot of typos in my markdown cells.

I found a work-around that enables spell checking in the markdown cells of my notebooks from GitHub user
[dsblank](https://github.com/dsblank) in the comments of the IPython project issue
[here](https://github.com/ipython/ipython/issues/3216). It is a bit hack-y and tedious but it works.

To enable spell checking, do the following:

1. Install a custom extension with the following command

		ipython install-nbextension https://bitbucket.org/ipre/calico/downloads/calico-spell-check-1.0.zip

2. Execute the following code in a cell of your notebook

		%%javascript
		IPython.load_extensions('calico-spell-check')

You should now see a new button in the tool bar that, when checked, enables spell checking within your markdown cells.

This functionality will only last for the current session of the current notebook. You'll have to repeat step 2 for each
notebook and for every session. **And be sure to delete or comment the code from step 2 once you've executed it.** I've
found that it causes problems (unexecutable markdown cells) if you happen to execute that block of code twice in one
session.

Apart from the tedium of this solution, I've found that it works rather well. Hopefully this functionality will make it
into future release of the IPython notebook.
