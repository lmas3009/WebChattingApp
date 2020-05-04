import seaborn as sns
dataset=[]
a=[]
def hello():
    iris = sns.load_dataset('iris')
    return iris.head().to_html()