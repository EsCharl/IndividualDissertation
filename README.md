# IndividualDissertation

A Snake game environment with training enabled using evolutionary algorithm. A trained model is included in this submission.

##### _python and additional python library used:_

1. python == 3.10.8
2. scipy == 1.10.1
3. pygame == 2.1.3dev8
4. matplotlib == 3.6.3
5. numpy == 1.24.1

### to start training or game.

1. launch "ScreenSelection.py" in the folder Menu to begin.

### to evaluate the performance of the trained model or the accumulated algorithm. 

###### Note: to evaluate the model parameter file (result.txt) must be present in the Learning folder.

###### Additionally: step 1 to 4 can be skipped if using the files provided in the supplimentary zip file titled "Score", to use the supplementary files just add all the files in the "Score" folder and place them into Evaluation/Score folder in the project folder.

1. modify the input parameter in the "EvaluationFramework.py" in line 174 to switch between model or accumulate algorithm.
2. if model is selected, to change between steps generated first or generated on demand by uncommenting line 92 and commenting line 93 for steps generated first. For steps generated on demand is by commenting 92 and uncommenting 93. 
3. run the file "EvaluationFramework.py".
4. to plot the graph, repeat for all the three evaluations (accumulated algorithm, model (moves generated first and generated on demand). 
5. modify lines 106, 121, and 140 in the file "StatisticalAnalysis.py" in the main folder to the file name specified in the evaluation made in the steps above. (the file names are in the folder Evalutaion/Score). 
6. run the file "StatisticalAnalysis.py" for the graphs

### to see overfitting or underfitting of the model.

###### Note: the model parameter file (result.txt) must be present in the Learning folder.

1. add the folders that are in the supplimentary zip file titled "data" into the folder of "data" in the project. (if wanted to add any additional files generate more instances use the "learn" feature of this project and stop the progress after the data generation stage has completed (the pygame screen closes)).
2. run the python file "EvalOverfittingOrUnderfitting.py" in Learning folder. this will generate text files based on each generation best parameters given in the "result.txt" in the Learning folder.
3. once the whole process is completed. run "OverfitorUnderfitBarChart.py" in Learning folder for the barchart.