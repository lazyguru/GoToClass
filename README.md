GoToClass
=============

Sublime Text Plugin to open the class file of the highlighted name.  Works in ST2 and ST3


### Usage
-----

* Highlight My_Special_Class_File, right click, choose "Go To Class", and it will select My/Special/Class/File using the fuzzy search
* Highlight `IdentityInterface`, right click, choose "Go To Qualified Class", and
	it will select `Magento\Framework\DataObject\IdentityInterface` using the
	fuzzy search (Name will be generated according to 'use' and 'namespace'
	statements)
* Press "Go To Parent Class" keybinding, and it will select parent class My/Special/Class/File using the fuzzy search
* Highlight My_Function, right click, choose "Go To Function", and it will select My_Function using the fuzzy search prefixed with '@'
* Highlight My_Data, right click, choose "Go To Data", and it will select My_Data using the fuzzy search prefixed with '#'

### Keybindings

Go To Class

	Mac OS X: CTRL+CMD+O
	Windows:  CTRL+ALT+O
	Linux:    CTRL+ALT+O

Go To Qualified Class

	Mac OS X: CTRL+SHIFT+CMD+O
	Windows:  CTRL+SHIFT+ALT+O
	Linux:    CTRL+SHIFT+ALT+O

Go To Parent Class

	Mac OS X: SUPER+SHIFT+O
	Windows:  CTRL+SHIFT+O
	Linux:    CTRL+SHIFT+O

Go To Function

	Mac OS X: SUPER+SHIFT+R
	Windows:  CTRL+SHIFT+R
	Linux:    CTRL+SHIFT+R

Go To Data

	Mac OS X: SUPER+SHIFT+;
	Windows:  CTRL+SHIFT+;
	Linux:    CTRL+SHIFT+;

### Settings
    go_to_class_separator: the separator between words in the class name. Default is "_"
