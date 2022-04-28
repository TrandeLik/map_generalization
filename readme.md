# Implementation of algorithm for generalization of cartographic objects 

Here is an implementation of map generalization algorithm (The idea is described [_**here**_](https://www.semanticscholar.org/paper/Fractal-and-Computational-Geometry-for-Generalizing-Edelsbrunner-Musin/36ad28df1593df9a9354b68a1b31a9bba63b4db1)).
There are following directories and files:
- *graphical_app.py* - simple demonstrative app. In it you can generate random polyline and watch results of 5 main steps:
    - Bringing a polyline to an equidistant form
    - Polyline segmentation
    - Douglas-Peucker simplification
    - Smoothing with B-splines
  
    Also you can read polyline from file to work with your own data.
    Please, generate polylines which has less than 120 vertexes, because default settings and generation algorithm guarantee correctness only with such number of vertexes
- *console_app.py* - the same app, but without graphics
- *logic* - the algorithm itself. All computations and geometry
- *settings* - settings of developed applications
- *data* - some additional data such as results of tests and dots of real cartographic objects
- *presentation* - presentation for joint scientific seminar INM RAS - Huawei
### Future work
- Implementing real-time scaling in graphical app (with simplification and without)
- Implementing canvas movement for correct drawing of large polylines
- Implementing new algorithms of random polylines generation
- Implementing graphical interface for settings
- Implementing simplified polyline saving
- Answering questions, which are mentioned in the presentation
- Further research
![Screenshot from 2022-04-28 15-37-08_cut-photo ru (1)](https://user-images.githubusercontent.com/42346736/165828657-bb62d543-1519-451b-947e-f2bc57b1c19b.png)
