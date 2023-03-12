import copy


def updateOtherAlgo(main_algo, algo1, algo2, algo3, algo4):
    algo1.body = copy.copy(main_algo.body)
    algo2.body = copy.copy(main_algo.body)
    algo3.body = copy.copy(main_algo.body)
    algo4.body = copy.copy(main_algo.body)

    algo1.defeated = False
    algo2.defeated = False
    algo3.defeated = False
    algo4.defeated = False
    main_algo.defeated = False


def updateOtherFood(main_food, algo1food, algo2food, algo3food, algo4food):
    algo1food.foodX = main_food.foodX
    algo1food.foodY = main_food.foodY

    algo2food.foodX = main_food.foodX
    algo2food.foodY = main_food.foodY

    algo3food.foodX = main_food.foodX
    algo3food.foodY = main_food.foodY

    algo4food.foodX = main_food.foodX
    algo4food.foodY = main_food.foodY


def clearSteps():
    return [], [], [], [], []


def resetDefeat():
    return False, False, False, False, False
