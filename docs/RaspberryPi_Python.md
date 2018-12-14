# Your first python Script!

# What is python!

Python is an interpreted, high-level programming language for general-purpose programming.
It provides constructs that enable clear programming on both small and large scales

# How to program using the Terminal Window

Opena a terminal widows with keys **Ctrl+Alt+T**

Create a new file
type `nano` in the command line to open the text editor.

If you know other text editors, you can use your preferred one

![pick](pictures/python_nano.png)

copy the following text:
You can also find it here [HelloWorld.py](../scripts/HelloWorld.py)
```
#! /usr/bin/python

#this is a comment
#import the librery time
import time
print("Hello IoT World")
time.sleep(5)
print("Goodbye IoT World")
```

To exit and save the changes press **Ctrl+X**. Select **Y** to save and type the name of the file ** "HelloWorld.py" **.

You can check the file with the command `cat HelloWorld.py`

Now you can run the script and see what happens
```
python HelloWorld.py
```



