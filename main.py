from psutil import Process
import os
from metrices.metrices import Metrices
from processEvaluation.evaluationController import EvaluationController


def main():
    ec = EvaluationController("6824",5)
    ec.run()
    ec.Terminate()


if __name__ == "__main__":
    main()
