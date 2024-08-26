Notes:

When Manually Creating 2 Binary Masks, we figured that it's not the accurate representation of the volume of the activated Tissue (VTA) and hence currently trying to find the intersection over ROI to get a modified use of the Jaccard Index.


## Models

1) Linear Regression

Without accounting for the covariates: 

- Right Side Model R-squared: 0.054650964102222144
- Right Side Model Mean Squared Error: 1356.871503790033
- Left Side Model R-squared: 0.007917060233980533
- Left Side Model Mean Squared Error: 1423.9698038522508

With accounting for the covariates: 

- Right Side Model R-squared: 0.09433099291316693
- Right Side Model Mean Squared Error: 1299.9182533834178
- Left Side Model R-squared: 0.08260030107615812
- Left Side Model Mean Squared Error: 1316.7744519816022

3) K-means clustering

