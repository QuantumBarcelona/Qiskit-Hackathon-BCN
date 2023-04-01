# **IBM Challenge: Visual State Preparation**

You are a new Quantum Researcher and have a great idea on what you can do with images on a Quantum Computer. (Maybe an algorithm for image recognition, or a quantum machine learning approach for image generation, or something else entirely).

Before you can start, working on this algorithm, however, you must first find a good way to encode images on a Quantum Computer.
You will follow the typical steps any researcher does, when having to prepare a quantum state, and solve all problems which you encounter along the way.
And since you will work with small images, you can get direct visual feedback and dont have to analyse a probability distribution.

## **Step 1: Find a way to decode and encode an image**

You will write 2 functions, one which will encode an 8x8 pixel image (greyscale so no colours) into a quantum circuit, and a second one, which will decode the results of a run of a circuit (run by a simulator) into an image.
You are free to use any method you want for example the ones which are in the Qiskit textbook or the one represented in this paper: https://arxiv.org/pdf/2112.01646.pdf

You will first use a simulator to implement your 2 methods (the encoding of the image as a quantum state and decoding the quantum state back into an image), this way you can directly test if it is correct: If you receive the same image as you started with, your code is correct.

## **Step 2: Finding a better representation of the state**

After you can decode and encode an image using a simulator, it becomes time to test this also on an actual Quantum Computer.
For this you first need to prepare the states in a better way.
Try to bring down the depth of the above generated circuits, since if your circuits have a too big depth, you will mostly just get noise from the quantum computer.
Try to test your method first with a simulator which includes noise, before you run it on the real device.
And feel free to “simplify” your image if needed.

*[Most encodings of images, like jpgs change the image (quality becomes slightly worse), so of course you can do the same, if this helps you to get a better result on the Quantum Computer]*

## **Step 3: Improving your results.**

Running the circuits alone rarely gives good results, which will most likely be seen after step 2. What you can do to improve your results is to apply post processing and some error mitigation (for example using runtime).
Of course, you can also try to optimize the circuits/representation further.
Now as you have seen how the whole process works, you might even try to find another way to encode and decode the image, after having understood the whole process a bit better.

This step is important when working with actual devices and gives you an impression, what quantum researchers have to deal with.