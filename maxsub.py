import sys
import math


def get_max_norep_sub(sent):
    if len(sent) < 1:
        return ""
    # curindex is the last index of the current substr
    curindex = maxindex = 0
    curlen = maxlen = 1

    for curindex in range(1, len(sent)):
        # check if the next char repeated in the current substr
        repeatindex = sent.find(sent[curindex], curindex - curlen, curindex)
        if repeatindex < 0:
            curlen += 1
            if curlen > maxlen:
                maxlen = curlen
                maxindex = curindex
                # print ("(%d %d)" % (maxlen, maxindex))
        else:
            curlen = curindex - repeatindex

    return sent[maxindex - maxlen + 1:maxindex + 1]


def test_maxsub():
    while (True):
        content = input("Please input the string to find out the substring without repeated character:\n")
        if content.lower() == "quit":
            sys.exit()
        print("The substring is:" + get_max_norep_sub(content))


class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self._capacity = capacity
        self._currentnum = 0
        self._head = None
        self._tail = None
        self._keymap = {}

    def get(self, key):
        """
        :rtype: int
        """
        findpair = self._keymap.get(key)
        if findpair is None:
            return -1
        else:
            self._movetohead(findpair)
            return findpair[0]

    def set(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: nothing
        """
        findpair = self._keymap.get(key)
        if findpair is None:
            pairtoadd = [value, None, None]
            self._keymap[key] = pairtoadd
            self._addtohead(pairtoadd)
        else:
            findpair[0] = value
            self._movetohead(findpair)

    def _addtohead(self, pairtoadd):
            if self._head is not None:
                pairtoadd[2] = self._head
                self._head[1] = pairtoadd
            self._head = pairtoadd

            if self._tail is None:
                self._tail = pairtoadd

            if self._currentnum == self._capacity:
                self._keymap.pop(self._tail[0])
                self._tail = self._tail[1]
            else:
                self._currentnum += 1

    def _movetohead(self, findpair):
            if findpair is self._head:
                return
            if findpair is self._tail:
                self._tail = self._tail[1]

            #pick up from the linked list
            prvpair = findpair[1]
            nxtpair = findpair[2]
            if prvpair is not None:
                prvpair[2] = nxtpair
            if nxtpair is not None:
                nxtpair[1] = prvpair
            #put to the first of the link
            findpair[2] = self._head
            findpair[1] = None
            self._head[1] = findpair
            self._head = findpair

    def testprint(self):
        print(self._keymap)
        print(self._head)
        print(self._tail)
        print("================")

def test_lru():
    cache = LRUCache(10)
    cache.set(10, 20)
    cache.set(11, 22)
    cache.set(12, 24)
    cache.testprint()

    cache.set(13,26)
    cache.get(10)
    cache.testprint()



class Solution(object):
    def maximumGap(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        num_len = len(nums)
        if num_len <= 1:
            return 0;
        num_max = max(nums)
        num_min = min(nums)

        if num_len == 2:
            return num_max - num_min
        bulk_size = (num_max - num_min) / (num_len - 1)
        if bulk_size == 0:
            return 0
        bulks = []
        bulk_min = num_min
        for index in range(num_len - 1):
            bulks.append([bulk_min + bulk_size, bulk_min])
            bulk_min += bulk_size
        bulks.append([num_max, num_max])  # for safty, avoid index overflow

        for num in nums:
            bulk_index = math.floor((num - num_min) / bulk_size)
            print("bulk_index:%d" % (bulk_index))
            if num > bulks[bulk_index][1]:
                bulks[bulk_index][1] = num
            if num < bulks[bulk_index][0]:
                bulks[bulk_index][0] = num

        # max_gap should span the bulks
        max_gap = cur_max_gap = 0
        prev_bulk_max = num_max

        for bulk in bulks:
            if bulk[0] > bulk[1]:  # empty bulk
                pass
            else:
                cur_max_gap = bulk[0] - prev_bulk_max
                tmp = prev_bulk_max
                prev_bulk_max = bulk[1]
                if cur_max_gap > max_gap:
                    max_gap = cur_max_gap
                    gap_first = tmp
                    gap_last = bulk[0]

        print("(%d, %d)" % (gap_first, gap_last))
        return max_gap

    def letterCombinations(self, digits):
        dletters = {'0':[' '],
                    '1':['*'],
                    '2':['a', 'b', 'c'],
                    '3':['d', 'e', 'f'],
                    '4':['g', 'h', 'i'],
                    '5':['j', 'k', 'l'],
                    '6':['m', 'n', 'o'],
                    '7':['p', 'q', 'r', 's'],
                    '8':['t', 'u', 'v'],
                    '9':['w', 'x', 'y', 'z']
                    }
        dsize = {'0':1, '1':1, '2':3, '3':3, '4':3, '5':3, '6':3, '7':4, '8':3, '9':4}

        num = 1
        for d in digits:
            num *= dsize[d]

        res = []
        for i in range(num):
            str = ""
            val = i
            for d in digits:
               (val, index) = divmod(val, dsize[d])
               str += dletters[d][index]
            res.append(str)

        return res


    def maxProfit2(self, prices):
        if len(prices) ==0:
            return 0
        cur_pro = 0
        cur_low = prices[0]
        cur_high = prices[0]
        for price in prices:
            if price >= cur_high:
                cur_high = price
            else:
                cur_pro += (cur_high - cur_low)
                cur_low = cur_high = price

            if price < cur_low:
                cur_low = price

        cur_pro += (cur_high - cur_low)
        return cur_pro




    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        if len(prices)==0:
            return 0

        max_pro = 0
        buy_pri = prices[0]
        sell_pro = 0
        for price in prices:
            if price < buy_pri:
                buy_pri = price
            else:
                sell_pro = price - buy_pri
            if sell_pro > max_pro:
                max_pro = sell_pro

        return max_pro


def findMaximumXOR(self, nums):
    answer = 0
    for i in range(32)[::-1]:
        answer <<= 1
        prefixes = {num >> i for num in nums}
        answer += any(answer ^ 1 ^ p in prefixes for p in prefixes)
    return answer

def mergeSort(arr, left, right):
    if right > left:
        mid = left + (right - left) // 2
        if mid > left:
            mergeSort(arr, left, mid)
        if right > mid + 1:
            mergeSort(arr, mid+1, right)

        tmp_arr = []
        left_iter = left
        right_iter = mid + 1
        for i in range(left, right +1):
            if  right_iter > right or (arr[left_iter] <= arr[right_iter] and left_iter <= mid):
                tmp_arr.append(arr[left_iter])
                left_iter += 1
            else:
                tmp_arr.append(arr[right_iter])
                right_iter += 1
        print("--------------------------")
        print(arr[left:right+1])
        print(tmp_arr)
        print("============================")
        for i in range(left, right +1):
            arr[i] = tmp_arr[i-left]



def split_2_arr(arr1, arr2):
    len1 = len(arr1)
    len2 = len(arr2)
    if len1 < len2:
        start_arr = arr2
        follow_arr = arr1
    else:
        start_arr = arr1
        follow_arr = arr1

    if len(follow_arr) == 0:
        print(start_arr)
        return

    magn = len(start_arr) // len(follow_arr)
    remain = len(start_arr) % len(follow_arr)

    outarr = []
    start_iter = 0
    for i in range(len(follow_arr)):
        for j in range(magn):
            outarr.append(start_arr[start_iter])
            start_iter += 1
        if remain > 0:
            outarr.append(start_arr[start_iter])
            start_iter += 1
            remain -= 1
        outarr.append(follow_arr[i])

    print("".join(outarr))



if __name__ == "__main__":
    testarr = [15252, 16764, 27963, 7817, 26155, 20757, 3478, 22602, 20404, 6739, 16790, 10588, 16521, 6644, 20880,
               15632, 27078, 25463, 20124, 15728, 30042, 16604, 17223, 4388, 23646, 32683, 23688, 12439, 30630, 3895,
               7926, 22101, 32406, 21540, 31799, 3768, 26679, 21799, 23740]
    sol = Solution()

    print (sol.maxProfit3([1,2,4,2,5,7,2,4,9,0]))

    #test_lru()
    #print(sol.maximumGap(testarr))
    #  print(sol.maximumGap([3,6,9,1]))
#    print(sol.letterCombinations("12345"))
