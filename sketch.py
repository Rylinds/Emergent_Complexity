import math
import vsketch

class RadialNoiseSketch(vsketch.SketchClass):
    '''
    Creating radial tree rings via Perlin noise and vsketch

    ----------

    VARIABLES:
    * noise_offset = shifts the sampleing circle away from the origin of noise-space.
        * without it, you get a symmetrical shape (lattice structure of noise algo).

    * noise_scale = controls the frequency of the noise
    (how quickly values change while moving through noise-space).
        * lower values are smooth.
        * higher values are rapid.

    * n_layer = first dimension of 3D noise lookup. It separates each concentric layer
    so they sample from different slices of noise (each ring has a unique shape).

    * n_x = second dimension of noise lookup (driven by `cos(angle)`).

    * n_y = thid dimension of noise lookup (driven by `sin(angle)`).

    * `*100` = increases the radius of the sampling circle in noise space
    (more 'bumps' around each ring; hardcoded).
    '''

    radius = vsketch.Param(0.200)
    points = vsketch.Param(360)
    layers = vsketch.Param(10)

    noise_scale = vsketch.Param(0.001)
    noise_offset = vsketch.Param(10)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size('letter', landscape=True)
        vsk.scale('cm')

        for layer in range(1, self.layers + 1):
            circle_points = []

            for point in range(self.points):
                angle = point * math.pi / 180

                n_layer = layer * self.noise_scale
                n_x = (self.noise_offset + math.cos(angle)) * self.noise_scale * 100
                n_y = (self.noise_offset + math.sin(angle)) * self.noise_scale * 100
                noise = vsk.noise(n_layer, n_x, n_y)

                x = (self.radius * layer) * math.cos(angle) * noise
                y = (self.radius * layer) * math.sin(angle) * noise

                circle_points.append((x, y))

            vsk.polygon(circle_points, close=True)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype('linemerge linesimplify reloop linesort')

#if __name__ == '__main__':
   #RadialNoiseSketch.display()
