## Algorithm settings
These files responsible for algorithm settings. In **generalization_settings.ini** you can change following parameters:
- Random polyline generation params:
  - MIN_X, MIN_Y, MAX_X, MAX_Y - coordinates of top-left and bottom-right dot
  - GENERATION_RATIO - coefficient of how "flattened" generated line will be
- Algorithm params
    - C - normalization constant for radius of equidistant polyline
    - N_INIT - initial number of segments in segmentation
    - N_P - minimal number of points in every segment after segmentation
    - N_S - maximum number of segments after segmentation
    - F - constant for extremal vertexes accounting
    - k - amount of dots in Minkowski dimension computing 
- Computational params
    - EPS - accuracy of floating point computation
    - DIGITS_COUNT - rounding constant
- Scaling parameters
    - m - scale
    - c_h - scaling normalization constant