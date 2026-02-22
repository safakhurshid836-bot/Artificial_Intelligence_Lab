# sort sent in alphabetical order

data="My Name Is Safa"

# ->ALPHABETS WORDS SORTING
words=data.split()
words.sort()
join=" ".join(words)
print(f'Alphabets words sorting: {join}')




#IMNSaaaefmsy -> ASCII CHARACTER SORTING
data="My Name Is Safa"
sorted_data=''.join(sorted(data))
print(f'ASCII Character sorting: {sorted_data}')

#Is My Name Safa-> ASCII WORDS SORTING
data="My Name Is Safa"
words=data.split()
sorted_words=" ".join(sorted(words))
print(f'ASCII Words sorting: {sorted_words}')
