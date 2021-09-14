import os
import time
import asyncio

path = r"C:\Users\Checkout\Documents\CMPE_273\Labs\Lab1\input"

outputpath = r"C:\Users\Checkout\Documents\CMPE_273\Labs\Lab1\output"


def mergeSort(arr):
    if len(arr) > 1:

        mid = len(arr) // 2

        L = arr[:mid]

        R = arr[mid:]

        mergeSort(L)

        mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


final_result = []


async def read_write(filename):
    file_path = f"{path}\{filename}"
    await asyncio.sleep(0.1)
    f = open(file_path)
    contents = f.readlines()
    for line in contents:
        final_result.append(int(line))
    f.close()


async def sort():
    start = time.time()
    print("Sorting.....")
    os.chdir(path)
    resultList = list()
    for file in os.listdir():
        resultList.append((read_write(file)))
    await asyncio.gather(*resultList)

    mergeSort(final_result)

    if  not os.path.exists(outputpath):
        os.mkdir(outputpath)

    textfile = open(f"{outputpath}\\async_sorted.txt", "w")
    for element in final_result:
        textfile.write(str(element) + "\n")
    textfile.close()
    end = time.time()
    print(f"Total execution time is {end - start}")


if __name__ == "__main__":
    asyncio.run(sort())
