import math

class Sorter:
    def bubblesort(self, test):
        list = test # how to init a list and add the entire input list????
        for iter_num in range(len(list) - 1, 0, -1):
            for idx in range(iter_num):
                if list[idx] > list[idx + 1]:
                    temp = list[idx]
                    list[idx] = list[idx + 1]
                    list[idx + 1] = temp
        return list

    def merge(self, left_half, right_half):

        res = []
        while len(left_half) != 0 and len(right_half) != 0:
            if left_half[0] < right_half[0]:
                res.append(left_half[0])
                left_half.remove(left_half[0])
            else:
                res.append(right_half[0])
                right_half.remove(right_half[0])
        if len(left_half) == 0:
            res = res + right_half
        else:
            res = res + left_half
        return res

    def merge_sort(self, test):
        unsorted_list = test
        if len(unsorted_list) <= 1:
            return unsorted_list
        middle = len(unsorted_list) // 2
        left_list = unsorted_list[:middle]
        right_list = unsorted_list[middle:]

        left_list = self.merge_sort(left_list)
        right_list = self.merge_sort(right_list)
        return self.merge(left_list, right_list)

    def insertion_sort(self, test):
        InputList = test
        for i in range(1, len(InputList)):
            j = i - 1
            nxt_element = InputList[i]
            while (InputList[j] > nxt_element) and (j >= 0):
                InputList[j + 1] = InputList[j]
                j = j - 1
            InputList[j + 1] = nxt_element
        return InputList

    def shellSort(self, test):
        input_list = test
        gap = math.floor(len(input_list) / 2)
        while gap > 0:
            for i in range(gap, len(input_list)):
                temp = input_list[i]
                j = i
                while j >= gap and input_list[j - gap] > temp:
                    input_list[j] = input_list[j - gap]
                    j = j - gap
                input_list[j] = temp
            gap = math.floor(gap / 2)
        return input_list


list = [64, 34, 25, 12, 22, 11, 90]
print(list)
sorter = Sorter()
test1 = sorter.bubblesort(list)
test2 = sorter.merge_sort(list)
test3 = sorter.insertion_sort(list)
test4 = sorter.shellSort(list)
print(test1)
print(test2)
print(test3)
print(test4)
print(list)