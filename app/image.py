from pathlib import Path

import cv2
import numpy as np
import numpy.typing as t


class SilhouetteFabric:
    def __init__(self):
        self.registry = {}

    @staticmethod
    def _get_silhouette_path(path: Path) -> Path:
        """
        Returns path to image's silhouette image.

        :param path:
        :return:
        """
        return path.parent / f"{path.stem}-binary.png"

    @staticmethod
    def _read_image(path: Path) -> t.NDArray:
        """
        Read image matrix

        :param path:
        :return:
        """
        return cv2.imread(str(path.resolve()), -1)

    @staticmethod
    def _write_image(path: Path, im: t.NDArray) -> bool:
        """
        Write image matrix to an image file

        :param path:
        :param im:
        :return:
        """
        return cv2.imwrite(str(path.resolve()), im)

    @staticmethod
    def _convert_to_binary(im: t.NDArray) -> t.NDArray:
        """
        Using image matrix fill in anywhere that is transparent or has alpha with
        white color and anywhere without alpha channel with black color.

        :param im:  Image matrix
        :return:    Updated image matrix
        """
        # fill non-alpha channel with black color.
        im[np.where(im[:, :, 3] != 0)] = (0, 0, 0, 255)
        # fill alpha channel with white color
        im[np.where(im[:, :, 3] == 0)] = (255, 255, 255, 255)
        # write binary image to a file
        return im

    def create_silhouette(self, path: Path) -> Path:
        """
        Create a binary silhouette of an image.

        :param path:    path to the image
        :return:        path to silhouette image
        """
        if path.name in self.registry:
            return self.registry[path.name]

        im = self._read_image(path)
        im = self._convert_to_binary(im)
        silhouette_path = self._get_silhouette_path(path)
        self._write_image(silhouette_path, im)
        self.registry[path.name] = silhouette_path
        return silhouette_path
