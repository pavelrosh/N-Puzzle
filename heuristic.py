class Heuristic:
    def __init__(self, current_node, final_node):
        self.current_node = current_node
        self.final_node = final_node

    def misplaced(self):
        current = [y for x in self.current_node.puzzle for y in x]
        final = [y for x in self.final_node.puzzle for y in x]
        h_score = 0
        i = 0
        while i < len(current):
            if current[i] != final[i] and current[i] != 0:
                h_score += 1
            i += 1
        # print(current)
        # print(final)
        # print(h_score)
        return h_score

    # def __del__(self):
    #     print("Heuristic vsyio.")
