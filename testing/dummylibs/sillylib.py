from random import randint

sillynames = ["Owen", "Clarkson", "Hammond", "[insert subject name here]", "Bob", "011000100110111101100010011101110110010101101110"]
sillydescs = ["blithering idiot", "orangutan", "heel-crested stork-like waterbird", "pajama monster of Traal", ]

def silly():
    name = sillynames[randint(0, len(sillynames)-1)]
    desc = sillydescs[randint(0, len(sillydescs)-1)]
    print(f"{name} you {desc}!")
