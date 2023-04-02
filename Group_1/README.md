# Qbit Enjoyers - Group 1

We converted an image into a 8x8 array we named it 'woman8.png'
"_image2heights(image)" converts the input image into an array of heights (amplitudes) in the gray scale
"height2circuit(height, log=False, eps=1e-2)" converts the heights into a normalized state, which we then convert to real circut using the transpiler.
Using the optimization level 3 we are getting a near similar image.
