import argparse
import json
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
import os
import warnings

from cellpose import models, plot


def main(inputs, img_path, img_format, output_dir):
    """
    Parameter
    ---------
    inputs : str
        File path to galaxy tool parameter
    img_path : str
        File path for the input image
    img_format : str
        One of the ['tiff', 'png', 'jpg']
    output_dir : str
        Folder to save the outputs.
    """
    warnings.simplefilter('ignore')

    with open(inputs, 'r') as param_handler:
        params = json.load(param_handler)

    img = skimage.io.imread(img_path)

    # transpose to Ly x Lx x nchann
    if img_format == 'tiff' and img.ndim == 3:
        img = np.transpose(img, (1, 2, 0))

    model_selector = params['model_selector']
    model_type = model_selector['model_type']
    chan = model_selector['chan']
    chan2 = model_selector['chan2']

    model = models.Cellpose(gpu=False, model_type=model_type)

    options = params['options']
    options.pop('flow_threshold')
    options.pop('cellprob_threshold')
    
    import inspect
    print(inspect.getargspec(model.eval))

    masks, flows, styles, diams = model.eval(img, channels=[chan, chan2],
                                             **options)

    # save masks to tiff
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        skimage.io.imsave(os.path.join(output_dir, 'cp_masks.tif'),
                          masks.astype(np.uint16))

    # make segmentation show
    maski = masks
    flowi = flows[0]
    fig = plt.figure(figsize=(12, 3))
    # can save images (set save_dir=None if not)
    plot.show_segmentation(fig, img, maski, flowi)
    fig.savefig(os.path.join(output_dir, 'segm_show.png'), dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-i", "--inputs", dest="inputs", required=True)
    aparser.add_argument("-p", "--img_path", dest="img_path")
    aparser.add_argument("-f", "--img_format", dest="img_format")
    aparser.add_argument("-O", "--output_dir", dest="output_dir")
    args = aparser.parse_args()

    main(args.inputs, args.img_path, args.img_format, args.output_dir)
