# Projet du cours RIW
projet du cours RIW. Projet RIW. OSY, CentraleSupélec

## How to request a query?
1. Clone this projet to your computer
2. Open the root folder of this project
3. Open the file SearchQueries.py
4. replace the "query" variable (line 15) by your own query. You could also modify the value of "output_number_max" and "threshold" to change the number of output files
5. Run and you will see the list of recommended documents in the console(descending pertinence)

## How to reconstruct the evaluation?
Please use the functions in "Evaluation.py" file to reconstruct our figures in the documentation or to explore more!
Uncomment the function and wait for the output.  

### Documentation of the evaluation functions
***evaluate(id,nb,thredhold)***  
**Description**: Given a query id number, number of output and the threshold, print the number of correct files,the precision and rappel value  
**Parameters**:  
  id: id number of the develop query. Integer number among 0 - 8 where id=0 means evaluating all 8 develop queries. By default 0
  nb: number of output files of a query, by default 100.
  threshold: threshold of the score. Only files with scores below the threshold will be output. threshold=0 is a particular case which we define it as no threshold. by default threshold=0
  
***evaluate_threshold(id,nb,threshold)***  
**Description**:  
Similar to evaluate but plotting the cumulative curves of pertinent and non-pertinent files as well as the precision curve,interpolated precision curve and rappel curve.  
**Parameters**:     
  id: id number of the develop query. Integer number among 0 - 8 where id=0 means evaluating all 8 develop queries. By default 0
  nb: number of output files of a query, by default 100000.
  threshold: threshold of the score. Only files with scores below the threshold will be output. threshold=0 is a particular case which we define it as no threshold. by default threshold=0
  
***evaluate_num(id,nb)***
**Description**:  
evaluate the precision and rappel with respect to a given develop query.
**Parameters**:  
  id: id number of the develop query. Integer number among 0 - 8 where id=0 means evaluating all 8 develop queries. By default 0
  nb: number of maximal output files of a query, by default 100.
  
 ***plotPrecisionRappel(id)***    
**Description**:  
plot the precision-rappel curve of a given develop query.  
**Parameters**:  
  id: develop query id number. Integer number among 0 - 8 where id=0 means evaluating all 8 develop queries.

## small documentation
Please check file 'PetitDocument.pdf'


