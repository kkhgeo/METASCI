# Environmental Science Spatiotemporal Scale Guide

Specifying spatiotemporal scale in an environmental science Introduction is essential.
The scale of research determines result interpretation and generalizability.

## Spatial Scales

| Scale | Range | Examples | Role in Introduction |
|-------|-------|----------|---------------------|
| Site/Plot | < 1 km² | Experimental plots, monitoring stations | P4: Study design description |
| Catchment/Watershed | 1-1,000 km² | Watersheds, small ecosystems | P2: System context |
| Regional | 1,000-100,000 km² | Nations, biomes | P1-P2: Domain setting |
| Continental | 100,000+ km² | Continents, ocean basins | P1: Broad context |
| Global | Entire Earth | Global change, climate system | P1: Opening sentence |

## Temporal Scales

| Scale | Range | Examples | Role in Introduction |
|-------|-------|----------|---------------------|
| Event | Minutes-days | Storms, floods | P2: Process description |
| Seasonal | Months-seasons | Growing season, wet/dry | P2: Pattern introduction |
| Interannual | 1-10 years | ENSO, variability | P1-P2: Trend setting |
| Decadal | 10-100 years | Climate change detection | P1: Long-term trends |
| Geological | 100+ years | Paleoclimate, evolution | P1: Historical context |

## Application in Blueprint

Must be included in `<blueprint_metadata>` of Stage 1 Blueprint:

```
- Spatiotemporal Scale: [Spatial: site/catchment/regional/continental/global] / [Temporal: event/seasonal/interannual/decadal/geological]
```

## Expression Patterns for Introduction

### Spatial scale introduction
- "At the catchment scale, ..."
- "Across regional gradients spanning ..."
- "Global-scale analyses have revealed ..."

### Temporal scale introduction
- "Over decadal timescales, ..."
- "Seasonal dynamics in ... exhibit ..."
- "Long-term monitoring (>10 years) has demonstrated ..."

### Scale mismatch as Gap framing
- "While plot-level experiments demonstrate X, ecosystem-scale responses remain uncharacterized"
- "Short-term studies (<5 years) show Y, but decadal trajectories are unknown"
- "Remote sensing captures broad spatial patterns, yet local heterogeneity in Z is poorly resolved"
