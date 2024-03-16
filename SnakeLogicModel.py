from SnakeLogic import SnakeLogic


class SnakeLogicModel(SnakeLogic):
    def getCoordinate(self, step):

        forward_holder = [self.body[0][0] - self.body[1][0], self.body[0][1] - self.body[1][1]]
        forward = [forward_holder[0] + self.body[0][0], self.body[0][1] + forward_holder[1]]

        # if the forward is downwards
        if forward_holder == [0, 1]:
            # left
            if step == 0:
                return [self.body[0][0] + 1, self.body[0][1]]
            elif step == 1:
                return forward
            else:
                return [self.body[0][0] - 1, self.body[0][1]]

        # if the forward is upwards.
        elif forward_holder == [0, -1]:
            # left
            if step == 0:
                return [self.body[0][0] - 1, self.body[0][1]]
            elif step == 1:
                return forward
            # right
            else:
                return [self.body[0][0] + 1, self.body[0][1]]

        # if the forward is rightwards.
        elif forward_holder == [1, 0]:
            # left
            if step == 0:
                return [self.body[0][0], self.body[0][1] - 1]
            elif step == 1:
                return forward
            # right
            else:
                return [self.body[0][0], self.body[0][1] + 1]

        # if the forward is leftwards.
        elif forward_holder == [-1, 0]:
            # left
            if step == 0:
                return [self.body[0][0], self.body[0][1] + 1]
            elif step == 1:
                return forward
            # right
            else:
                return [self.body[0][0], self.body[0][1] - 1]