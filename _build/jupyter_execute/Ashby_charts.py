# Ashby charts for acoustics education
#### Matthew  C M Wright, ISVR, University of Southampton

Material selection charts, often called Ashby charts, are scatter plots whose axes represent two different properties of a material. As well as their utility for practising engineers they have educational value, allowing students to visualise the differences between classes of materials. In this notebook I show how an Ashby chart for fluids, showing properties of interest to acousticians, can be constructed, and discuaa how they can be used in an educational setting.

The code is written in Python 3 using the following libraries:
 - NumPy for array manipulation
 - Pandas for data handling 
 - Plotly Express for visualisation

import numpy as np
import pandas as pd
from plotly import express as px

## Data
The accompanying spreadsheet `Fluid properties.xlsx` contains information about 85 fluids. It was obtained from Wolfram Alpha's curated data, and gives (I infer) properties at NTP (20 °C, 1 atm = 101.325 kPa). Eventually I'll use one of the wrappers to REFPROPs to pull in data under specified conditions. 

It can be read into a pandas dataframe. 

fluids = pd.read_excel('Fluid properties.xlsx', 'Sheet1', index_col = 0)

This creates a dataframe object called `fluids`. The last argument tells us to use the first column (the name of the substance) as the index.  We can look at the first few substances:

fluids.head()

The dataframe can be interrogated using indexes, booleans and dataframe methods. For example, the five densest gases can be found as follows.

fluids[fluids['Phase'] == 'gas'].sort_values(by = 'Density')[-5:]

A particular proprty of a particular fluid can be extracted like this:

fluids.loc['Air', 'Density']

## Visualization

Interrogating and visualizing this data set can form the basis for a lesson, an activity or a project. Some suggestions are given below that illustrate the possibilities.

An obvious question to ask is how sound speed varies with density. We can plot it like this:

fig = px.scatter(fluids, 
                 x = "Density", 
                 y = "Sound speed",
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Sound speed": "Sound speed [m/s]"},
                 color = "Phase", 
                 hover_name = fluids.index, 
                 template = "plotly_white")
fig.show()

An immediate lesson is that liquids and gases can have the same sound speed at NTP.

Students can explore the chart by hovering on data points ro reveal substances name, and find that water has the highest sound speed in the data set. They might also notice that the liquid refrigerants (with R numbers) form a separate cluster from the other organic liquids and could edit the spreadsheet so as to colour them differently.

Changing `hover_name = fluids.index` to `text = fluids_index` will display the names of each substance on the chart. This will be crowded, but the zoom and pan tools can then be used to explore particular regions of the chart. Using the mouse to drag a box around a region zooms to that region; double-clicking restores the original axes. Elements of the chart can be removed and restotored by clicking on their labels in the legend.

Another obvious conclusion is that on a linear scale the gas densities are hard to distinguish, prompting the use of a logarithmic scale. We'll also highlight the points for air and water since those are most often needed.

fig = px.scatter(fluids, 
                 x = "Density", 
                 y = "Sound speed",
                 log_x = True,
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Sound speed": "Sound speed [m/s]"},
                 color = "Phase", 
                 hover_name = fluids.index, 
                 template = "plotly_white")

fig.add_scatter(x = [fluids.loc["Water", "Density"]],
                y = [fluids.loc["Water", "Sound speed"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Water",
                hovertext = "Water")

fig.add_scatter(x = [fluids.loc["Air", "Density"]],
                y = [fluids.loc["Air", "Sound speed"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Air",
                hovertext = "Air")

fig.show()

The fact that the gases now cluster about a curve might prompt  a comparison with the ideal gas law prediction $c = \sqrt{\gamma P/\rho}$ for, say, monatomic and diatomic gases. 

P = 101.325e3
gamma_monatomic = 5/3
gamma_diatomic =  7/5
rho = np.logspace(-1.1, 1, 100)

fig = px.scatter(fluids, 
                 x = "Density", 
                 y = "Sound speed",
                 log_x = True,
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Sound speed": "Sound speed [m/s]"},
                 color = "Phase", 
                 hover_name = fluids.index, 
                 template = "plotly_white")

fig.add_scatter(x = [fluids.loc["Water", "Density"]],
                y = [fluids.loc["Water", "Sound speed"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Water",
                hovertext = "Water")

fig.add_scatter(x = [fluids.loc["Air", "Density"]],
                y = [fluids.loc["Air", "Sound speed"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Air",
                hovertext = "Air")

fig.add_scatter(x = rho, 
                y = np.sqrt(gamma_monatomic*P/rho),
                name = "Ideal monatomic gas")

fig.add_scatter(x = rho, 
                y = np.sqrt(gamma_diatomic*P/rho),
                name = "Ideal diatomic gas")

fig.show()

Making both axes logarithmic, of course, makes the ideal-gas relationship a straight line.

fig = px.scatter(fluids, 
                 x = "Density", 
                 y = "Sound speed",
                 log_x = True,
                 log_y = True,
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Sound speed": "Sound speed [m/s]"},
                 color = "Phase", 
                 hover_name = fluids.index, 
                 template = "plotly_white")

fig.add_scatter(x = [fluids.loc["Water", "Density"]],
                y = [fluids.loc["Water", "Sound speed"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Water",
                hovertext = "Water")

fig.add_scatter(x = [fluids.loc["Air", "Density"]],
                y = [fluids.loc["Air", "Sound speed"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Air",
                hovertext = "Air")

fig.add_scatter(x = rho, 
                y = np.sqrt(gamma_monatomic*P/rho),
                name = "Ideal monatomic gas")

fig.add_scatter(x = rho, 
                y = np.sqrt(gamma_diatomic*P/rho),
                name = "Ideal diatomic gas")

fig.show()

Another property to explore is the fluid's isentropic bulk modulus (the inverse of its compressibility), given by  $B = \rho_0 c^2$.

We can add it as a new column in the dataframelike this:

fluids['Bulk modulus'] = fluids['Density']*fluids['Sound speed']**2

We can use this to create an 'Acoustic Ashby chart' with bulk modulus vs density.

fig = px.scatter(fluids, 
                 x = "Density", 
                 y = "Bulk modulus",
                 log_x = True,
                 log_y = True,
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Bulk modulus": "Bulk modulue [Pa]"},
                 color = "Phase", 
                 hover_name = fluids.index, 
                 template = "plotly_white")

fig.add_scatter(x = [fluids.loc["Water", "Density"]],
                y = [fluids.loc["Water", "Bulk modulus"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Water",
                hovertext = "Water")

fig.add_scatter(x = [fluids.loc["Air", "Density"]],
                y = [fluids.loc["Air", "Bulk modulus"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Air",
                hovertext = "Air")

fig.show()

A single-phase version can be generated either by 'switching off' liquid and water in the figure above, or as follows, where each gas is also  labelled.

fig = px.scatter(fluids[fluids['Phase'] == 'gas'], 
                 x = "Density", 
                 y = "Bulk modulus",
                 log_x = True,
                 log_y = True,
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Bulk modulus": "Bulk modulus [Pa]"},
                 color = "Phase", 
                 text = fluids[fluids['Phase'] == 'gas'].index,
                 template = "plotly_white")

fig.add_scatter(x = [fluids.loc["Air", "Density"]],
                y = [fluids.loc["Air", "Bulk modulus"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Air",
                hovertext = "Air")

fig.show()

At this point, students could be asked to use the ideal gas law to determine which gases are monatomic.

## Bulk modulus

Returning to the two-phase Ashby chart, we can determine both sound speed $c$ and characteristic specific acoustic impedance $z$ ('impedance' hereafter for brevity) from the axis variables. Specifically

$$
c = \sqrt{B/\rho}, \qquad z = \sqrt{B\rho},
$$

so contours of $c$ and $z$ will be perpendicular diagonal lines on the chart. Plotting contours of $\log_{10} c$ and $\log_{10} z$ allows them to be evenly spaced on the logarithmic axes; labelling them and turning off their hover information allows the substance information to still be seen when hovering.

rho = np.logspace(-1.3, 3.5, 50)
b = np.logspace(4.5, 10, 50)

RHO, B = np.meshgrid(rho, b)

z = np.sqrt(B*RHO)
c = np.sqrt(B/RHO)
c_squared = B/RHO

fig = px.scatter(fluids, 
                 x = "Density", 
                 y = "Bulk modulus",
                 log_x = True,
                 log_y = True,
                 labels = 
                     {"Density": "Density [kg/m^3]",
                      "Bulk modulus": "Bulk modulus [Pa]"},
                 color = "Phase", 
                 hover_name = fluids.index, 
                 template = "plotly_white")

fig.add_scatter(x = [fluids.loc["Water", "Density"]],
                y = [fluids.loc["Water", "Bulk modulus"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Water",
                hovertext = "Water")

fig.add_scatter(x = [fluids.loc["Air", "Density"]],
                y = [fluids.loc["Air", "Bulk modulus"]],
                mode = "markers",
                marker = {"size": 8},
                name = "Air",
                hovertext = "Air")

fig.add_contour(x = rho, 
                y = b, 
                z = np.log10(z),
                name = "log10(z [rayl])",
                contours = {"coloring": "none",
                           "start": 2,
                           "end": 6,
                           "size": 1,
                           "showlabels": True},
               hoverinfo = "skip")

fig.add_contour(x = rho, 
                y = b, 
                z = np.log10(c),
                name = "log10(c [m/s])",
                contours = {"coloring": "none",
                           "start": 0,
                           "end": 6,
                           "size": 1,
                           "showlabels": True},
               line = {"color": "Blue"},
               hoverinfo = "skip")

fig.show()

This acoustic Ashby chart makes it clear that while gases and liquids can have the same sound speed their impedances areabout three orders of magnitude apart.

If we used data or models that accounted for the variation of these properties with, say, temperature then it would be possible to animate the Ashby chart and see the points move as conditions change.  

