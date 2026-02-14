### Disturbed Concentric Cicles
#### Define a Cicle
1. Create a 360-sided polyogon
2. Add concentric circles
3. Add a little bit of noise?
```
# doing it the wrong way
noise = vks.noise(layer * self.noise_scale, point * self.noise_scale)
x = self.radius * layer * math.cos(angle) * noise
y = self.radius * layer * math.sin(angle) * noise
1
```
This skews the circles in an organic way, but this causes the circle to not complete the loop.

To fix the noise: rather than applying layer and degree, you need to account for the layer and x and y coordinates *independently*. 
* sample the noise function along a circular path in noise-space.
```
noise_offset = 7        # arbitrary number

# sample noise on a circle so it loops naturally
n_layer = layer * self.noise_scale
n_x = (noise_offset + math.cos(angle)) * self.noise_scale * 100
n_y = (noise_offset + math.sin(angle)) * self.noise_scale * 100

noise = nsk.noise(n_layer, n_x, n_y)
```
* noise_offset = shifts the sampleing circle away from the origin of noise-space. 
    * without it, you get a symmetrical shape (lattice structure of noise algo).
* noise_scale = controls the frequency of the noise (how quickly values change while moving through noise-space).
    * lower values are smooth.
    * higher values are rapid.
* n_layer = first dimension of 3D noise lookup. It separates each concentric layer so they sample from different slices of noise (each ring has a unique shape).
* n_x = second dimension of noise lookup (driven by `cos(angle)`).
* n_y = thid dimension of noise lookup (driven by `sin(angle)`).
* `*100` = increases the radius of the sampling circle in noise space (more 'bumps' around each ring; hardcoded).