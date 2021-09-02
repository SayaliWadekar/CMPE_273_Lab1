# cmpe273-lab1

# Following output was seen after executing ext_merge_sort.py
# Sorting.....
# Total execution time is 0.013390779495239258

# real	0m0.300s
# user	0m0.479s
# sys	0m0.139s

#Following output was seen after executing async_merge_sort.py
#Sorting.....
#Total execution time is 0.11708211898803711

#real	0m0.191s
#user	0m0.083s
#sys	0m0.008s

# From the above output we can conclude that async operation takes less time as compare to the sync operation. Here as the file size is small there is lot of overhead for io operatins
# when using asyncio. That is why to simulate large file operation  wait time is added.
