import RT_utility as rtu
import numpy as np
from PIL import Image as im
import math
import RT_pbar
import multiprocessing


class Renderer():

    def __init__(self, cCamera, iIntegrator, sScene) -> None:
        self.camera = cCamera
        self.integrator = iIntegrator
        self.scene = sScene
        self.num_cores = multiprocessing.cpu_count()

    def _render_row(self, j):
        row_data = []
        for i in range(self.camera.img_width):

            pixel_color = rtu.Color(0, 0, 0)

            for spp in range(self.camera.samples_per_pixel):
                generated_ray = self.camera.get_ray(i, j)
                pixel_color = pixel_color + \
                    self.integrator.compute_scattering(
                        generated_ray,
                        self.scene,
                        self.camera.max_depth
                    )

            row_data.append(pixel_color)

        return j, row_data

    def _render_row_jittered(self, j):
        row_data = []
        sqrt_spp = int(math.sqrt(self.camera.samples_per_pixel))

        for i in range(self.camera.img_width):

            pixel_color = rtu.Color(0, 0, 0)

            for s_j in range(sqrt_spp):
                for s_i in range(sqrt_spp):
                    generated_ray = self.camera.get_jittered_ray(
                        i, j, s_i, s_j
                    )
                    pixel_color = pixel_color + \
                        self.integrator.compute_scattering(
                            generated_ray,
                            self.scene,
                            self.camera.max_depth
                        )

            row_data.append(pixel_color)

        return j, row_data

    def render(self):

        self.scene.find_lights()

        renderbar = RT_pbar.start_animated_marker(
            self.camera.img_height * self.camera.img_width
        )

        with multiprocessing.Pool(processes=self.num_cores//2) as pool:

            results = pool.imap_unordered(
                self._render_row,
                range(self.camera.img_height)
            )

            for j, row_data in results:
                for i, pixel_color in enumerate(row_data):
                    self.camera.write_to_film(i, j, pixel_color)
                    renderbar.update(j * self.camera.img_width + i)

    def render_jittered(self):

        self.scene.find_lights()

        renderbar = RT_pbar.start_animated_marker(
            self.camera.img_height * self.camera.img_width
        )

        with multiprocessing.Pool(processes=self.num_cores//2) as pool:

            results = pool.imap_unordered(
                self._render_row_jittered,
                range(self.camera.img_height)
            )

            for j, row_data in results:
                for i, pixel_color in enumerate(row_data):
                    self.camera.write_to_film(i, j, pixel_color)
                    renderbar.update(j * self.camera.img_width + i)


    def write_img2png(self, strPng_filename):
        png_film = self.camera.film * 255
        data = im.fromarray(png_film.astype(np.uint8))
        data.save(strPng_filename)