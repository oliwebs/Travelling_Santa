# Travelling_Santa
Kaggle competition entry for the Travelling Santa problem.

This algorithm takes inspiration from the A* search algorithm. The A* search algorithm favours steps that have minimal Euclidean distance to the final destination. As the problem in this scenario requires a route that visits every point, the rule is edited so that the algorithm will choose the point that has the shortest distance to another point immediately after. Therefore, the algorithm - to some extent - favours "clusters" of points.

https://www.kaggle.com/c/traveling-santa-2018-prime-paths
