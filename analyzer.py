import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n")

product_code = input("Please enter product code: ")


opinions = pd.read_json(f'./opinions/{product_code}.json')
print(opinions)
max_score = 5

opinions['stars'] = (opinions['score']*max_score).round(1)

# opinions_count = len(opinions)
opinions_count = opinions.shape[0]
pros_count  = opinions.pros.astype(bool).sum()
cons_count  = opinions.cons.astype(bool).sum()
avarage_score = (opinions.score.mean()*max_score).round(2)

print(f"""For the product with {product_code} product_code:
      There is {opinions_count} opininom posted.
      For {pros_count} opinions the list at product advantages is given
      and for {cons_count} opinions the list at product disadvntages is given
      The avarage score for the product is {avarage_score}.""")

if not os.path.exists("./charts"):
    os.mkdir("./charts")
recommendations = opinions.recommendation.value_counts(dropna=False).reindex([True,False,np.nan], fill_value=0)

print(recommendations)

recommendations.plot.pie(
    label="",
    labels = ["Recommend", "Not recommend", "Neutral"],
    colors = ["green", "red", "grey"],
    autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '' 
    
    )
plt.title("Recommendation")
plt.savefig(f"./charts/{product_code}_pie.png")
plt.close()

stars = opinions.stars.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
print(stars)
stars.plot.bar(color = "pink")
plt.ylim(0,max(stars)+10)

plt.title("Star count distribution")
plt.xlabel("Number of stars")
plt.ylabel("Number of opinions")
plt.xticks(rotation = 0)
plt.grid(True, "major", "y")
for index, value in enumerate(stars):
    plt.text(index, value +1.5, str(value), ha = 'center')
plt.show()
