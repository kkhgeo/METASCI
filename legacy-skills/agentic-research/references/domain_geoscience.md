# Domain Reference: Geoscience & Environmental Science

Guidance for applying the agentic research framework to geoscience datasets.

## Common Dataset Types

### Geochemistry
- **Major/trace elements**: XRF, ICP-MS/OES data (wt%, ppm)
- **Isotope ratios**: Sr, Nd, Pb, O, C isotopic compositions
- **REE patterns**: Chondrite/PAAS-normalized rare earth elements
- **Mineral chemistry**: EPMA, LA-ICP-MS spot analyses

### Environmental Monitoring
- **Water quality**: pH, DO, conductivity, nutrient concentrations
- **Sediment cores**: Depth profiles with multi-proxy data
- **Atmospheric data**: Particulate matter, gas concentrations, meteorology
- **Remote sensing**: Satellite-derived indices (NDVI, LST, etc.)

### Spatial/Temporal Data
- **Time series**: Monitoring station records, paleoclimate proxies
- **Spatial grids**: Gridded geochemical surveys, interpolated maps
- **Core/profile data**: Depth-resolved measurements

## Cycle 1 Recommendations (EDA)

For geoscience datasets, the first cycle should always include:

1. **Compositional check**: Geochemical data are compositional (sum to ~100%).
   - Apply log-ratio transforms (CLR, ILR) before multivariate analysis
   - Avoid raw correlation on compositional data (spurious correlations)

2. **Detection limits**: Check for values at/below analytical detection limits
   - Flag censored data; consider substitution or Kaplan-Meier methods

3. **Spatial/temporal structure**: Check for autocorrelation
   - Variogram analysis for spatial data
   - ACF/PACF for time series

4. **Quality control**: 
   - Standard reference material (SRM) reproducibility
   - Duplicate analysis precision
   - Closure check for major elements

## Statistical Approaches by Data Type

### Geochemical Classification
- **Discriminant diagrams**: TAS, AFM, tectonic discrimination
- **Multivariate**: PCA on CLR-transformed data
- **Clustering**: K-means, hierarchical, DBSCAN on normalized compositions
- **Machine learning**: Random forest for provenance/classification

### Environmental Trend Analysis
- **Mann-Kendall test**: Non-parametric trend detection
- **Sen's slope**: Robust trend magnitude estimation
- **Changepoint detection**: PELT, BOCPD for regime shifts
- **Seasonal decomposition**: STL for periodic signals

### Spatial Analysis
- **Kriging**: Spatial interpolation with uncertainty
- **Moran's I**: Spatial autocorrelation test
- **GWR**: Geographically weighted regression
- **Hotspot analysis**: Getis-Ord Gi*

### Isotope Mixing
- **Binary/ternary mixing models**: End-member identification
- **Bayesian mixing**: MixSIAR, simmr for source apportionment
- **Monte Carlo error propagation**: Uncertainty in mixing calculations

## Hypothesis Generation Patterns

Common hypothesis types in geoscience that the framework should explore:

1. **Source identification**: "Element X enrichment indicates source Y"
   - Test: Compare with known source signatures, discriminant analysis
   - Literature: Search for regional geochemical baselines

2. **Process control**: "Process A controls the distribution of variable B"
   - Test: Correlation, regression with mechanistic covariates
   - Literature: Thermodynamic/kinetic constraints

3. **Temporal change**: "Variable X shows a significant trend over period Y"
   - Test: Mann-Kendall, breakpoint analysis
   - Literature: Known environmental drivers

4. **Spatial pattern**: "Anomaly Z is associated with geological feature W"
   - Test: Spatial statistics, overlay analysis
   - Literature: Regional geological context

## Literature Search Strategy

Effective search queries for geoscience literature:

- **Geochemistry**: "[element] [rock type] [tectonic setting] geochemistry"
- **Environmental**: "[contaminant] [media] [region] assessment"
- **Isotopes**: "[isotope system] [application] [geological context]"
- **Methods**: "[analytical technique] [matrix] [analyte] detection limit"

Priority databases: Google Scholar, GeoRef, Web of Science, Scopus
Key journals: GCA, Chemical Geology, EPSL, Environmental Science & Technology,
Science of the Total Environment, Applied Geochemistry

## Python Libraries

Commonly needed for geoscience analysis:

```python
# Core
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Geoscience-specific
# pip install pyrolite  — compositional data, petrological diagrams
# pip install scikit-learn  — ML classification, clustering
# pip install pymannkendall  — Mann-Kendall trend test
# pip install ruptures  — changepoint detection
# pip install geopandas  — spatial data
# pip install pykrige  — kriging
```

## Guardrails for Geoscience

1. **Compositional data closure**: Never run PCA/correlation on raw wt% data
2. **Detection limits**: Report how censored data were handled
3. **Analytical uncertainty**: Include propagated errors in interpretations
4. **Sample size**: Many geoscience datasets are small (n<30). Use non-parametric tests.
5. **Geological context**: Statistical patterns need geological plausibility
6. **Spatial pseudoreplication**: Nearby samples are not independent
