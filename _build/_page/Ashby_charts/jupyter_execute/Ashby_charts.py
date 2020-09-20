# Ashby charts for fluids and strings

**Matthew C M Wright** [mcmw@isvr.soton.ac.uk](mailto:mcmw@soton.ac.uk)

Updated 2020-09-20

----

## Introduction

[Material selection charts](http://www-materials.eng.cam.ac.uk/mpsite/interactive_charts/), often called Ashby charts, are scatter plots whose axes represent two different properties of a material. They often show categories of materials e.g. woods, metals, rather than individual material. 

By overlaying contours of some desirable property function of the axis variables one can identify the material with the highest value of that property. For example, Schelleng {cite}`schelleng_1963` showed that sound radiation from violins should be proportional to $\sqrt{E/\rho^3}$ where $E$ is Young's modulus and $\rho$ is density. Superimposing contours of this function over an Ashby chart with these axes indicates that woods have better sound radiation properties than other available materials. 

```{margin}
It also revealed that balsa wood has the highest $\sqrt{E/\rho^3}$ of commmon woods. This was tested when Waltham {cite}`waltham_2009` made a balsa violin and showed that, aesthetic considerations aside, its sound radiation predictions were indeed in line with expectations.
``` 

Logarithmic axes allow a wide range of values to be displayed mean that contours of power-law functions appear as straight lines.

As well as their utility for practising engineers they have educational value, allowing students to visualise the differences between classes of materials. If students are provided with the means to construct such charts themselves they can explore and investigate the data for themseves. 
In this notebook I show how an Ashby chart for fluids, showing properties of interest to acousticians, can be constructed, and discuss how they can be used in an educational setting. The concept is then extended to musical strings.  

The code is written in Python 3 using the following libraries:
 - NumPy for array manipulation
 - Pandas for data handling 
 - Plotly Express for visualisation
 
Some of the less obvious aspects of the coding features are pointed out during the notebook, which provides a number of examples of Plotly Express usage, which may be of use to those using it for other tasks as some of the usage is not entirely straightforward. If, on the other hand, you know a better way to achieve the results here please let me know, either via email or github pull request. 

This is a work in progress; in particular I hope to add string data forr more instruments and would be glad to hear of sources of that information.

import numpy as np
import pandas as pd
import plotly.express as px

## Fluids
### Data
A CSV data file `Fluid properties.csv`, available in the GitHub repository, contains properties of a number of fluids at NTP (20°C, 1 atm = 101.325 kPa), obtained from the NIST Thermophysical Properties of Fluid Systems tool, which is based on Lemmon, McLinden and Friend's chapter in the NIST Chemistry WebBook {cite}`NIST`.
It can be read into a pandas dataframe as follows. 

fluids = pd.read_csv('Fluid properties.csv', index_col = 0)

This creates a dataframe object called `fluids`. The last argument assigns the leftmost column (containing the fluid names) to be the index of the dataframe (Python indexes start at zero).  We can look at the first few substances:

fluids.head()

The dataframe can be interrogated using indexes, booleans and dataframe methods. For example, the five densest gases can be found as follows.

fluids[fluids['Phase'] == 'gas'].sort_values(by = 'Density')[-5:]

Here 
 - `fluids[fluids['Phase'] == 'gas']` is a dataframe containing only gases due to its boolean index, 
 - `sort_values()` is a method available to dataframes whose keyword argument `by` determines the sort index, 
 - `[-5:]` is an index that specifies the last five elements of the list-like object it is appended to. 

It is possible to write e.g. `fluids.Density` instead of `fluids['Density]`, but this syntax cannot easily be extended to columns with spaces in their headings, so will not be used here.

The properties of a particular fluid can be extracted like this: 

fluids.loc['Air']

A particular property of a particular fluid can be extracted like this:

fluids.loc['Air']['Density']

Writing `fluids.loc['Air', 'Density']` would have the same effect.

An additional fluid can be added like this:

fluids.loc['Dodecafluoropentane'] = [10.31, 99.72, 'gas']

### Visualization

Interrogating and visualizing this data set can form the basis for a lesson, an activity or a project. Some suggestions are given below that illustrate the possibilities.

An obvious question to ask is how sound speed varies with density. We can plot it like this:

fig = px.scatter(fluids, 
                 x = 'Density', 
                 y = 'Sound speed',
                 labels = {'Density': 'Density [kg/m^3]',
                           'Sound speed': 'Sound speed [m/s]'},
                 color = 'Phase', 
                 hover_name = fluids.index, 
                 template = 'plotly_white')
fig.show()

```{margin} Axis labels
Without `labels` being set the column headings (which don't give units) would be automatically used as the axis labels. The dictionary supplied as the value for `labels` could also be written `dict([('Density', 'Density [kg/m^3]'), ('Sound speed', 'Sound speed [m/s]')])`.
```

To avoid having to set the template in future plots we can make it the default from now on. We will also set the default figure width.

px.defaults.template = 'plotly_white'
px.defaults.width = 700

Students can explore the chart by hovering on data points to reveal substances' names. Changing `hover_name = fluids.index` to `text = fluids.index` will display the names of each substance on the chart permanently.  This will be crowded, but the zoom and pan tools can then be used to explore particular regions of the chart. Using the mouse to drag a box around a region zooms to that region; double-clicking restores the original axes. 

#### Suggested activities:

The following examples of student activities cover a range of levels from in-class test to longer term project, and include physics, data visualization and coding. 
 1. Find the gas with the highest sound speed and the liquid with the lowest sound speed.
 3. Find the liquid and gas with the most similar sound speed, and give your definition of 'most similar'.
 4. Mercury is not included in the spreradsheet. Where on the chart would you expect it to lie (this could be a class discussion)? Once you have recorded your prediction(s), look up its properties and add it. 
 5. Do the same for seawater of a given salinity and/or air of a given humidity.
 5. Refrigerants are denoted by an R followed by their ASHRAE number{cite}`ASHRAE`. Modify the code to show refrigerants with a different colour, without editing the CSV file.
 6. Click on 'gas' in the legend; this will stop displaying the gases and rescale the axes appropriately. Identify any commonalities among liquids that are similarly arranged or clustered. Investigate possible reasons for this.    
 7. Turn the gases back on and the liquids off, and notice the curved shape of the envelope of points. Add the options `log_x = True` and `log_y = True` to the `px.scatter()` to show whether it follows a power law. Superimpose the ideal gas law prediction for sound speed $c = \sqrt{\gamma P/\rho}$ for monatomic ($\gamma = 5/3$) and diatomic ($\gamma = 7/5$) gases. 

The code required for the last of these is given below by way of a worked example.  The points corresponding to air and water are picked out in different colours with larger markers, because of their importance in acoustics applications. Hover information is turned off for the air and water highlights and the ideal gas law predictions, to avoid interfering with the fluid data-points. 



P = 101.325e3
gamma_monatomic = 5/3
gamma_diatomic = 7/5
rho = np.logspace(-1.1, 1, 100)

fig = px.scatter(fluids, 
                 x = 'Density', 
                 y = 'Sound speed',
                 hover_name = fluids.index, 
                 color = 'Phase', 
                 log_x = True,
                 log_y = True,
                 labels = 
                      {'Density': 'Density [kg/m^3]',
                       'Sound speed': 'Sound speed [m/s]'})

fig.add_scatter(x = [fluids.loc['Water', 'Density']],
                y = [fluids.loc['Water', 'Sound speed']],
                mode = 'markers',
                marker = {'size': 8},
                name = 'Water',
                hoverinfo = 'skip')

fig.add_scatter(x = [fluids.loc['Air', 'Density']],
                y = [fluids.loc['Air', 'Sound speed']],
                mode = 'markers',
                marker = {'size': 8},
                name = 'Air',
                hoverinfo = 'skip')

fig.add_scatter(x = rho, 
                y = np.sqrt(gamma_monatomic*P/rho),
                name = 'Ideal monatomic gas',
                hoverinfo = 'skip')

fig.add_scatter(x = rho, 
                y = np.sqrt(gamma_diatomic*P/rho),
                name = 'Ideal diatomic gas',
                hoverinfo = 'skip')

fig.show()

```{margin} Coding note
Data for `x` and `y` values has to be supplied as a dataframe column, an aray or a list, so when the single points for air and water are plotted the expressions that give the values are wrapped in brackets to make them single-element lists.
```

Static plots, for insertion into PowerPoint slides, for example, can be generated using the 'camera' icon above the chart.  The interactive html version can be saved with e.g. `fig.write_html('Acoustic_Ashby_chart.html')`. Specifying `width` and `height` will prevent the resulting figure from resizing and changing aspect ratio with the browser window.

### Bulk modulus

A change of axes provides a different view of the data. We can add a new column in the dataframe containing the fluid's isentropic bulk modulus $B = \rho c^2$ (the inverse of its compressibility) like this:

fluids['Bulk modulus'] = fluids['Density']*fluids['Sound speed']**2

We can use this to plot bulk modulus vs density.

```{margin}
<p style="margin-bottom:6cm;"> </p>
```

#```{margin}
#<p style="margin-bottom:6cm;"> </p>
#```
fig = px.scatter(fluids, 
                 x = 'Density', 
                 y = 'Bulk modulus',
                 color = 'Phase', 
                 hover_name = fluids.index,
                 log_x = True,
                 log_y = True,
                 labels = 
                      {'Density': 'Density [kg/m^3]',
                       'Bulk modulus': 'Bulk modulus [Pa]'})

fig.add_scatter(x = [fluids.loc['Water', 'Density']],
                y = [fluids.loc['Water', 'Bulk modulus']],
                mode = 'markers',
                marker = {'size': 8},
                name = 'Water',
                hoverinfo = 'skip')

fig.add_scatter(x = [fluids.loc['Air', 'Density']],
                y = [fluids.loc['Air', 'Bulk modulus']],
                mode = 'markers',
                marker = {'size': 8},
                name = 'Air',
                hoverinfo = 'skip')

fig.show()

#### Suggested activities
 1. Deduce from the ideal gas law where you expect monatomic gases to be located on this chart, and then check your prediction (turn the liquids off for easier viewing).
 2. In which direction(s) would the points move if the temperature increased and the pressure remained the same? 
 3. Plot contours of sound speed $c = \sqrt{B/\rho}$ and label them at appropriate intervals.
 4. Do the same for characteristic specific acoustic impedance $z = \rho c = \sqrt{B\rho}$.

The following code provides a worked example for the second and third of these. In fact contours of $\log_{10} c$ and $\log_{10} z$ are plotted, allowing them to be evenly spaced on the logarithmic axes. Additional contours (shown with dashed lines) pass through the data points for air and water.

```{margin}
<p style="margin-bottom:6cm;"> </p>
```

rho, B = np.logspace(-1.3, 4, 100), np.logspace(4.5, 10, 100)

rho_grid, B_grid = np.meshgrid(rho, B)

z = np.sqrt(B_grid*rho_grid)
c = np.sqrt(B_grid/rho_grid)

rho_air, c_air = fluids.loc['Air', ['Density', 'Sound speed']]
rho_water, c_water = fluids.loc['Water', ['Density', 'Sound speed']]

z_air, z_water = rho_air*c_air, rho_water*c_water

fig = px.scatter(fluids, 
                 x = 'Density', 
                 y = 'Bulk modulus',
                 color = 'Phase', 
                 hover_name = fluids.index,
                 log_x = True,
                 log_y = True,
                 labels = 
                      {'Density': 'Density [kg/m^3]',
                       'Bulk modulus': 'Bulk modulus [Pa]'})

fig.add_scatter(x = [fluids.loc['Water', 'Density']],
                y = [fluids.loc['Water', 'Bulk modulus']],
                mode = 'markers',
                marker = {'size': 8},
                name = 'Water',
                hoverinfo = 'skip')

fig.add_scatter(x = [fluids.loc['Air', 'Density']],
                y = [fluids.loc['Air', 'Bulk modulus']],
                mode = 'markers',
                marker = {'size': 8},
                name = 'Air',
                hoverinfo = 'skip')

fig.add_contour(x = rho, 
                y = B, 
                z = np.log10(z),
                name = 'log10(z [rayl])',
                contours = {'coloring': 'none',
                           'start': 2,
                           'end': 6,
                           'size': 1,
                           'showlabels': True},
               hoverinfo = 'skip')

fig.add_contour(x = rho, 
                y = B, 
                z = np.log10(c),
                name = 'log10(c [m/s])',
                contours = {'coloring': 'none',
                           'start': 0,
                           'end': 6,
                           'size': 1,
                           'showlabels': True},
               line = {'color': 'Blue'},
               hoverinfo = 'skip')

fig.add_contour(x = rho, 
                y = B, 
                z = np.log10(z),
                showlegend = False,
                contours = {'coloring': 'none',
                           'start': np.log10(z_air),
                           'end': np.log10(z_water),
                           'size': np.log10(z_water/z_air),
                           'showlabels': True},
                line = {'dash': 'dash'},
               hoverinfo = 'skip')

fig.add_contour(x = rho, 
                y = B, 
                z = np.log10(c),
                showlegend = False,
                contours = {'coloring': 'none',
                           'start': np.log10(c_air),
                           'end': np.log10(c_water),
                           'size': np.log10(c_water/c_air),
                           'showlabels': True},
               line = {'color': 'Blue',
                       'dash': 'dash'},
               hoverinfo = 'skip')

fig.show()

This diagram can be used to explore the normal incidence reflection and transmission between fluids with different impedances, for example, what reflection coefficient applies when the fluids are one, two or three impedance contours apart? It could also inform a discussion about the effect of gas bubbles on underwater sound. A more advanced programming exercise would be to animate the motion of data points with changing temperature.

Students could also gather data for solids to add to the chart, which could prompt a discussion on whether to use the solids' actual bulk modulus or its Young's modulus.

## Strings

For longitudinal sound waves in fluids the bulk modulus provides the restoring force that makes the fluid return to its equiliibrium state when disturbed; density provides the inertia that makes them take time to do so. Liquids are stiff and heavy, and lie at the top right of the chart; gases are floppy and light, and lie at the bottom left of the chart.

For transverse waves on strings, such as those on musical instruments, the restoring force is provided by the tension $\tau$ (newtons) provides the restoring force, and mass per unit length $\mu$ (kilograms per metre) provides the restoring force. Furthermore, wave speed and impedance (mechanical this time) bear the same relationship to $\tau$ and $\mu$ that their acoustic counterparts do to $B$ and $\rho$, i.e.

$$
c = \sqrt{\tau/\mu}, \qquad z = \sqrt{\tau\mu},
$$

(the symbols $c$ and $z$ will refer to strings for the remainder of this notebook). Therefore if we make an Ashby chart for strings, using $\mu$ and $\tau$ as the axes, the speed and impedance contours will be the same as they were for the fluids chart.

### Guitars

Another file has data for several sets of guitar strings. The data was obtained from the website of the D'Addario company, who helpfully provide tension data (in kg) for all the strings they sell (D'Addario undated).

strings_g = pd.read_csv('String data guitar.csv')
strings_g.head()

No `index_col` was specified when importing because there isn't a suitable column to use as an index. Pandas has therefore generated a numerical index. Each row corresponds to a different string, string sets are grouped together and strings are given in descending pitch order within sets.

The tension and scale can then be converted to SI units; we'll give these units in brackets rather than parentheses so that column names can be directly used as axis labels.

strings_g['Tension [N]'] = strings_g['Tension (kg)'] * 9.81
strings_g['Scale [m]'] = strings_g['Scale (cm)']/100

The mass per unit length is not provided, but can be inferred from the tension and the fundamental frequency. The note names, in Scientific Pitch Notation (SPN) are given according to standard tuning, and from these the fundamental frequencies can be calculated as follows, assumingg equal temperament.

note_names = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 
        'Gs', 'A', 'As', 'B']

for index, row in strings_g.iterrows():
    semitones = note_names.index(row['Note'][:-1])
    strings_g.loc[index, 'Frequency [Hz]'] = 440 * 2** \
           (int(row['Note'][-1]) - 4 + (semitones - 9)/12)

In `note_names` a sharp is designated by `s` rather than the usual sign. The conversion has to be done a row at a time because the string index that extracts the letter and number components of the SPN note-name cannot be broadcasted over dataframe columns.

The formula in the last line calculates the number of semitones the note in question is from A4, assumed to be at 440 Hz (`A` being the ninth element of `note_names`, counting from zero).

Having found the frequency $f$ the wave speed $c$ from the knowledge that string waves travels twice the length of the string $L$ in a period, so that $c = 2fL$. The mass per unit length can then be inferred by rearranging $c = \sqrt{\tau/\mu}$ to give $\mu = \tau/c^2 = \tau/4L^2f^2$. So-called 'scale length' varies slightly between guitars, but has been assumed, in the data, to be 64.5 cm for all guitars.

strings_g['Mass/length [kg/m]'] = strings_g['Tension [N]']/ \
     (4*(strings_g['Scale [m]'])**2 * strings_g['Frequency [Hz]']**2)

Strings from the same set can be shown as points joined by a line.
In order to group string sets together we must define a name that is unique to each set. The string code also be used for this purpose, but would be less informative in the chart's legend. Instead we combine multiple information fields.

#strings_g['Name'] = strings_g['Type'] + ' ' + \
#                    strings_g['Instrument'] + ' ' + \
#                    strings_g['String type']

strings_g['Name'] = strings_g['Type'] + ' ' + \
                    strings_g['String type']


Since the longer name occupies more space in the legend the overall default width should be increased.

#px.defaults.width = 900

If we assign the `color` of the data points to this `Name` column, and use lines as well as markers the points for individual strings will be joined up. Guitars, like most plucked string instruments, have all their strings the same length, but with differing weights so as to keep the tensions similar. We would therefore expect a set of guitar strings to make an approximately horizontal line when plotted with tension vs mass per unit length. We can test this conjecture.

```{margin}
<p style="margin-bottom:6cm;"> </p>
```

fig = px.scatter(strings_g, 
                 x = 'Mass/length [kg/m]', 
                 y = 'Tension [N]', 
                 color = 'Name',
                 log_x = True,
                 log_y = True)

fig.update_traces(mode = 'lines+markers')
    
fig.show()

The chart reveals that (for these string sets, at least):
 - For all but one set the top E-string is slightly tighter than its neighbour
 - For all sets the bottom E-string is slightly slacker than its neighbour
 - The variation in tension among the classical guitar string sets is much smaller than between the electric guitar sets, although the subjective difference is presumably significant

Steel-strung guitars, as is well known, either have additional bracing to withstand higher tension, or have solid bodies. Electric guitars can also tolerate lower tension than acoustic guitars because pickups respond to string velocity, which can be maintained independently of tension, rather than force on the bridge, which varies in proportion to tension.

Because all the strings are the same length all the notes tuned to a particular pitch must have the same wave-speed, and therefore lie on the same diagonal line. We can confirm this by joining up matching notes like this:

```{margin}
<p style="margin-bottom:6cm;"> </p>
```

fig = px.scatter(strings_g, 
                 x = 'Mass/length [kg/m]', 
                 y = 'Tension [N]', 
                 color = 'Name',
                 log_x = True,
                 log_y = True)

for i, note in enumerate(strings_g['Note'].unique()):
    note_set = strings_g[strings_g['Note'] == note]

    fig.add_scatter(x = note_set['Mass/length [kg/m]'], 
                    y = note_set['Tension [N]'],
                    name = note,
                    marker = {'color': 'Grey',
                              'size': 1},
                    hoverinfo = 'skip')

fig.update_traces(mode = 'lines+markers')
    
fig.show()

```{margin}
Setting the marker size to 1 pixel effectively hides it; instructions to set sizes to zero are ignored.
```

### Other instruments

A further file contains similar data for a range of instrument strings, including a subset of the guitar sets shown above. For instruments with re-entrant tunings, such as the higher ukuleles, strings are given in pitch order rather than strringing order. 

The data can be input and processed in a similar way to the guitar data.

strings = pd.read_csv('String data various.csv')

strings['Tension [N]'] = strings['Tension (kg)'] * 9.81
strings['Scale [m]'] = strings['Scale (cm)']/100

for i, row in strings.iterrows():
    semitones = note_names.index(row['Note'][:-1])
    strings.loc[i, 'Frequency [Hz]'] = 440 * 2** \
           (int(row['Note'][-1]) - 4 + (semitones - 9)/12)
    
strings['Mass/length [kg/m]'] = strings['Tension [N]']/ \
     (4*(strings['Scale [m]'])**2 * strings['Frequency [Hz]']**2)

strings['Name'] = strings['Type'] + ' ' + \
                                 strings['Instrument']
notype = pd.isnull(strings['Name'])
strings.loc[notype, 'Name'] = strings.loc[notype, 'Instrument']

```{margin}
Instruments without a type require their names to be constructed separately because a missing value is imported as a NaN ('Not a Number'), which would suppress plotting if included in the name.
```

For this set the string type is not included in the name to save space; most are medium apart from the electric guitar, which is light as these are widely used. 

The resulting chart can be produce as before, and contours of wavespeed and impedance can be added in the same way as for the fluids.

```{margin}
<p style="margin-bottom:6cm;"> </p>
```

mu = np.logspace(-3.7, -0.8, 100)
tau = np.logspace(1, 3, 100)

mu_grid, tau_grid = np.meshgrid(mu, tau)

z = np.sqrt(tau_grid*mu_grid)
c = np.sqrt(tau_grid/mu_grid)

fig = px.scatter(strings, 
                 x = 'Mass/length [kg/m]', 
                 y = 'Tension [N]', 
                 color = 'Name',
                 log_x = True,
                 log_y = True)

fig.update_traces(mode = 'lines+markers')

fig.add_contour(x = mu, 
                y = tau, 
                z = np.log10(z),
                name = 'log10(z [Ns/m])',
                contours = {'coloring': 'none',
                           'start': -2,
                           'end': 1,
                           'size': 0.5,
                           'showlabels': True},
               hoverinfo = 'skip')

fig.add_contour(x = mu, 
                y = tau, 
                z = np.log10(c),
                name = 'log10(c [m/s])',
                contours = {'coloring': 'none',
                           'start': 1,
                           'end': 3,
                           'size': 0.5,
                           'showlabels': True},
               line = {'color': 'Blue'},
               hoverinfo = 'skip')

fig.write_html('Strings_chart.html')

fig.show()

The slowest waves are on the bottom string of the electric bass, while the fastest are in the top string of the tenor guitar, slosely followed by the mandolin.

We can also use other combinations of properties to make charts, such as mass per unit length vs frequency.

fig = px.scatter(strings,
                 x = 'Frequency [Hz]', 
                 y = 'Mass/length [kg/m]',
                 color = 'Name',
                 log_x = True,
                 log_y = True,
                 width = 600)

fig.update_traces(mode = 'lines+markers')

fig.show()

The resulting points cluster in two regions. Plotting the same data but colouring it according to the excitation method...

fig = px.scatter(strings,
                 x = 'Frequency [Hz]', 
                    y = 'Mass/length [kg/m]',
                    hover_name = 'Name',
                    color = 'Method',
                    log_x = True,
                    log_y = True,
                    width = 600)

fig.show()

...reveals that these clusters largely correspond to plucked and bowed strings with two exceptions: the mandolin sits with the bowed strings and the erhu with the plucked strings. The mandolin is strung in pairs, but so is the oud (apart from its bottom string) and that sits at the edge of the plucked cluster tht is furthest from the bowed cluster.

Although tension is not explicitly plotted on this chart it implicitly enters via the identity $4f^2\mu = \tau/L^2$, and the restoring force at the plucking/bowing point will scale with $\tau/L$. 

Mass, tension and frequency can be shown on a 3d plot as follows.

fig = px.line_3d(strings, 
                 x = 'Mass/length [kg/m]', 
                 y = 'Tension [N]', 
                 z = 'Frequency [Hz]',
                 color = 'Name',
                 text = 'Instrument',                
                 log_x = True,
                 log_y = True,
                 log_z = True)

fig.update_traces(mode = 'lines+markers',
                  marker = {'size': 3})

fig.show()

Viewed on these axes  the bottom two strings of the mandolin and the violin are close, but the top two are further apart. 

Scale can also be used as the third axis, in which case each instrument's string-set will lie in a horizontal plane, with the exception of the banjo.

fig = px.line_3d(strings, 
                 x = 'Mass/length [kg/m]', 
                 y = 'Tension [N]', 
                 z = 'Scale [m]',
                 color = 'Name',
                 text = 'Instrument',                
                 log_x = True,
                 log_y = True,
                 log_z = True)

fig.update_traces(mode = 'lines+markers',
                  marker = {'size': 3})

fig.show()

The two instruments that lie closest on both sets of axes are the ruan and the tenor guitar. 

## Discussion and further work 

All these charts, whether for fluids or strings, are subjective in that their appearance depends on which candidates are included and excuded from the datasets. 

There are several instruments whose strings would be interesting to add to the string charts:
 - **Theorbo**: as well as having two scale lengths these have lower notes and longer strings than any instrument included so far.
 - **Harp**: 

It would also be interesting to add keyboard strings, i.e. clavichord, harpsichord, and piano. Furthermore it would be interesting to compare early wood-framed piano strings to modern iron-framed strings, and the 'short-scale' upright piano with the concert grand. It seems likely that the strings of a clavichord would be similar to those of a hammered dulcimer but it would be nice to confirm this.

## Conclusion

Taking an 'Ashby chart' approach to properties of interest to acousticians can provide useful insights that could be useful in acoustics education. 

```{bibliography} ./references.bib
```