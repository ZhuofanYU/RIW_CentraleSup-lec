from Utils.evaluation import *

if __name__ == "__main__":
    # plot the precision-rappel curve of query
    # plotPrecisionRappel(1)
    # plotPrecisionRappel(2)
    # plotPrecisionRappel(3)
    # plotPrecisionRappel(4)
    # plotPrecisionRappel(5)
    # plotPrecisionRappel(6)
    # plotPrecisionRappel(7)
    # plotPrecisionRappel(8)

    # Plot the synthesis graph according to the number of output files
    # evaluate_num(id=0, nb=5000)
    # evaluate_num(id=1, nb=5000)
    # evaluate_num(id=2, nb=5000)
    # evaluate_num(id=3, nb=5000)
    # evaluate_num(id=4, nb=500)
    # evaluate_num(id=5, nb=5000)
    # evaluate_num(id=6, nb=5000)
    # evaluate_num(id=7, nb=5000)
    # evaluate_num(id=8, nb=5000)

    # plot the synthesis graph of all 8 queries, time consuming
    # evaluate_threshold()

    # plot the synthesis graph of query 3, with threshold 1.344
    # evaluate_threshold(id=1)
    # evaluate_threshold(id=2)
    # evaluate_threshold(id=3)
    # evaluate_threshold(id=4)
    # evaluate_threshold(id=5)
    # evaluate_threshold(id=6)
    # evaluate_threshold(id=7)
    # evaluate_threshold(id=8)

    evaluate(id=0, nb=100)
    evaluate(id=1, nb=100)
    evaluate(id=2, nb=100)
    evaluate(id=3, nb=100)
    evaluate(id=4, nb=100)
    evaluate(id=5, nb=100)
    evaluate(id=6, nb=100)
    evaluate(id=7, nb=100)
    evaluate(id=8, nb=100)
