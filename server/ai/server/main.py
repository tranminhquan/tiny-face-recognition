

'''TO DO: Flask is implenmented here by Hai Nguyen'''


import sys
sys.path.append('..')

from models.cv.skippedvgg import SkippedVGG3Blocks

print(sys.path)

model = SkippedVGG3Blocks(include_top=True, input_shape=(144,192,3), classes=51, verbose=1)
