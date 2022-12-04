import numpy as np
import math
import matplotlib.pyplot as plt
def tensors_as_images(
    tensors, nrows=1, figsize=(8, 8), titles=[], wspace=0.1, hspace=0.2, cmap=None
):
    """
    Plots a sequence of pytorch tensors as images.
    :param tensors: A sequence of pytorch tensors, should have shape CxWxH
    """
    assert nrows > 0

    num_tensors = len(tensors)

    ncols = math.ceil(num_tensors / nrows)

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        gridspec_kw=dict(wspace=wspace, hspace=hspace),
        subplot_kw=dict(yticks=[], xticks=[]),
    )
    axes_flat = axes.reshape(-1)

    # Plot each tensor
    for i in range(num_tensors):
        ax = axes_flat[i]

        image_tensor = tensors[i]
        assert image_tensor.dim() == 3  # Make sure shape is CxWxH

        image = image_tensor.numpy()
        image = image.transpose(1, 2, 0)
        image = image.squeeze()  # remove singleton dimensions if any exist

        # Scale to range 0..1
        min, max = np.min(image), np.max(image)
        image = (image - min) / (max - min)

        ax.imshow(image, cmap=cmap)

        if len(titles) > i and titles[i] is not None:
            ax.set_title(titles[i])

    # If there are more axes than tensors, remove their frames
    for j in range(num_tensors, len(axes_flat)):
        axes_flat[j].axis("off")

    return fig, axes

def view_images_as_thumbnails(
    images, nrows=1, figsize=(8, 8), titles=[], wspace=0.1, hspace=0.2, cmap=None
):
    assert nrows > 0

    num_images = len(images)

    ncols = math.ceil(num_images / nrows)

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        gridspec_kw=dict(wspace=wspace, hspace=hspace),
        subplot_kw=dict(yticks=[], xticks=[]),
    )
    axes_flat = axes.reshape(-1)

    # Plot each tensor
    for i in range(num_images):
        ax = axes_flat[i]

        image = np.asarray(images[i])
      #  image = image.squeeze()  # remove singleton dimensions if any exist
        # Scale to range 0..1
        min, max = np.min(image), np.max(image)
        image = (image - min) / (max - min)

        ax.imshow(image, cmap=cmap)

        if len(titles) > i and titles[i] is not None:
            ax.set_title(titles[i])

    # If there are more axes than tensors, remove their frames
    for j in range(num_images, len(axes_flat)):
        axes_flat[j].axis("off")

    return fig, axes
