# Initial dataset
movies = [
    ("Eternal Sunshine of the Spotless Mind", 20000000),
    ("Memento", 9000000),
    ("Requiem for a Dream", 4500000),
    ("Pirates of the Caribbean: On Stranger Tides", 379000000),
    ("Avengers: Age of Ultron", 365000000),
    ("Avengers: Endgame", 356000000),
    ("Incredibles 2", 200000000)
]

print(">>> Movie Budget Analyzer <<<")

# to add movies
add_movie = input("Do you want to add more movies? (yes/no): ").strip().lower()

if add_movie == "yes":
    num_movies = int(input("How many movies do you want to add? "))
    
    for i in range(num_movies):
        print(f"Entering movie {i+1}")
        name = input("Movie name: ")
        budget = float(input("Movie budget: "))
        
        movies.append((name, budget))

# to calculate average budget
total_budget = 0

for movie in movies:
    total_budget += movie[1]   # movie[1] is the budget

average_budget = total_budget / len(movies)

# to add space 
print(f'')
print(f"Average Budget: ${average_budget:,.2f}")
# to add space
print(f'')

# to find high budget movies
count = 0

print("Movies with Above-Average Budget: ")

for movie in movies:
    name, budget = movie
    
    if budget > average_budget:
        difference = budget - average_budget
        print(f"{name}")
        print(f"  Budget: ${budget:,.2f}")
        print(f"  Above Average By: ${difference:,.2f}\n")
        count += 1

# to add space
print(f'')
print(f"Total movies above average: {count}")
print("Program Finished.")