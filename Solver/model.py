## example from devito/examples/seismic/tutorials


from devito import Grid, TimeFunction, Eq, Operator, solve
from examples.seismic import Model, plot_velocity, Receiver, TimeAxis, RickerSource, plot_shotrecord
import numpy as np
#%matplotlib inline

#First part: Define the physical problem

# Define a physical size
shape = (101, 101)  # Number of grid point (nx, nz)
spacing = (10., 10.)  # Grid spacing in m. The domain size is now 1km by 1km
origin = (0., 0.)  # What is the location of the top left corner. This is necessary to define
# the absolute location of the source and receivers


# Define a velocity profile. The velocity is in km/s
v = np.empty(shape, dtype=np.float32)
v[:, :51] = 1.5
v[:, 51:] = 2.5

# With the velocity and model size defined, we can create the seismic model that
# encapsulates this properties. We also define the size of the absorbing layer as 10 grid points
# nbl : The number of absorbin layers for boundary damping.
# bcs : Absorbing boundary type ("damp" or "mask") or initializer.
#vp : Velocity in km/s
model = Model(vp=v, origin=origin, shape=shape, spacing=spacing, space_order=2, nbl=10, bcs="damp")

#plot_velocity(model)


#Second part: Acquisition geometry



t0 = 0.  # Simulation starts a t=0
tn = 1000.  # Simulation last 1 second (1000 ms)
dt = model.critical_dt  # Time step from model grid spacing

time_range = TimeAxis(start=t0, stop=tn, step=dt)



f0 = 0.010  # Source peak frequency is 10Hz (0.010 kHz)
src = RickerSource(name='src', grid=model.grid, f0=f0,
                   npoint=1, time_range=time_range)

# First, position source centrally in all dimensions, then set depth
src.coordinates.data[0, :] = np.array(model.domain_size) * .5
src.coordinates.data[0, -1] = 20.  # Depth is 20m

# We can plot the time signature to see the wavelet
#src.show()




# Create symbol for 101 receivers
rec = Receiver(name='rec', grid=model.grid, npoint=101, time_range=time_range)

# Prescribe even spacing for receivers along the x-axis
rec.coordinates.data[:, 0] = np.linspace(0, model.domain_size[0], num=101)
rec.coordinates.data[:, 1] = 20.  # Depth is 20m

# We can now show the source and receivers within our domain:
# Red dot: Source location
# Green dots: Receiver locations (every 4th point)
#plot_velocity(model, source=src.coordinates.data, receiver=rec.coordinates.data[::4, :])


# Third Part: Finite-difference discretization

# In order to represent the wavefield u and the square slowness we need symbolic objects 
# corresponding to time-space-varying field (u, TimeFunction) and 
# space-varying field (m, Function)

# redefinition of v and model (both the same as before)

# Define the wavefield with the size of the model and the time dimension
u = TimeFunction(name="u", grid=model.grid, time_order=2, space_order=2)

# We can now write the PDE
pde = model.m * u.dt2 - u.laplace

# This discrete PDE can be solved in a time-marching way updating u(t+dt) from the previous time step
# Devito as a shortcut for u(t+dt) which is u.forward. We can then rewrite the PDE as 
# a time marching updating equation known as a stencil using customized SymPy functions
stencil = Eq(u.forward, solve(pde, u.forward))



# Finally we define the source injection and receiver read function to generate the corresponding code
src_term = src.inject(field=u.forward, expr=src * dt**2 / model.m)

# Create interpolation expression for receivers
rec_term = rec.interpolate(expr=u.forward)



op = Operator([stencil] + src_term + rec_term, subs=model.spacing_map)


op(time=time_range.num-1, dt=model.critical_dt)

print(op.ccode)

#plot_shotrecord(rec.data, model, t0, tn)

assert np.isclose(np.linalg.norm(rec.data), 370, rtol=1)