import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import random
from collections import Counter

df = pd.read_csv('./data/data.csv', encoding='latin-1')
df = df.dropna()
df = df.drop_duplicates()
total_data = df.shape[0]
negative_tweets = df[(df['HS'] ==1) | (df['Abusive'] ==1)]
positive_tweets = df[(df['HS'] ==0) & (df['Abusive'] ==0)]
HS_tweets = df[(df['HS'] ==1)]
total_HS_tweets = HS_tweets.shape[0]
total_negative_tweets = negative_tweets.shape[0]

def generateRandomColor(numberOfColor):
     color=["#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)])
       for j in range(numberOfColor)]
     return color

def getMostCommonWords(data: pd.DataFrame, numberOfCommonWords):
    p = Counter(" ".join(data).split()).most_common(numberOfCommonWords)
    result = pd.DataFrame(p, columns=['Kata', 'Frekuensi'])
    return result

def getMostCommonWordsInNegativeTweet():
    data = getMostCommonWords(negative_tweets['Tweet'], 10)
    return data

def getMostCommonWordsInPositiveTweet():
    data = getMostCommonWords(positive_tweets['Tweet'], 10)
    return data

def getMostCommonWordsInTweet():
    data = getMostCommonWords(df['Tweet'], 10)
    return data

def getDataInvidualHateSpeech():
    HS_Religion_tweets = df[(df['HS_Religion'] ==1) & (df['HS_Individual'] ==1)]
    HS_Race_tweets = df[(df['HS_Race'] ==1) & (df['HS_Individual'] ==1)]
    HS_Physical_tweets = df[(df['HS_Physical'] ==1) & (df['HS_Individual'] ==1)]
    HS_Gender_tweets = df[(df['HS_Gender'] ==1) & (df['HS_Individual'] ==1)]
    HS_Other_tweets = df[(df['HS_Other'] ==1) & (df['HS_Individual'] ==1)]
    df_HS_individual_tweets = pd.concat([HS_Religion_tweets, HS_Race_tweets, HS_Physical_tweets, HS_Gender_tweets, HS_Other_tweets])
    df_HS_individual_tweets = df_HS_individual_tweets.dropna()
    df_HS_individual_tweets = df_HS_individual_tweets.drop_duplicates()
    return df_HS_individual_tweets

def getDataGroupHateSpeech():
    HS_Religion_tweets = df[(df['HS_Religion'] ==1) & (df['HS_Group'] ==1)]
    HS_Race_tweets = df[(df['HS_Race'] ==1) & (df['HS_Group'] ==1)]
    HS_Physical_tweets = df[(df['HS_Physical'] ==1) & (df['HS_Group'] ==1)]
    HS_Gender_tweets = df[(df['HS_Gender'] ==1) & (df['HS_Group'] ==1)]
    HS_Other_tweets = df[(df['HS_Other'] ==1) & (df['HS_Group'] ==1)]
    df_HS_group_tweets = pd.concat([HS_Religion_tweets, HS_Race_tweets, HS_Physical_tweets, HS_Gender_tweets, HS_Other_tweets])
    df_HS_group_tweets = df_HS_group_tweets.dropna()
    df_HS_group_tweets = df_HS_group_tweets.drop_duplicates()
    return df_HS_group_tweets

def calculateIndividualHateSpeech():
    df_individual = getDataInvidualHateSpeech()
    HS_Religion_tweets = df_individual[(df_individual['HS_Religion'] ==1)]
    HS_Race_tweets = df_individual[(df_individual['HS_Race'] ==1)]
    HS_Physical_tweets = df_individual[(df_individual['HS_Physical'] ==1)]
    HS_Gender_tweets = df_individual[(df_individual['HS_Gender'] ==1)]
    HS_Other_tweets = df_individual[(df_individual['HS_Other'] ==1)]
    data = [
        {'Klasifikasi': 'Agama', 'Total': HS_Religion_tweets.shape[0]},
        {'Klasifikasi': 'Ras', 'Total': HS_Race_tweets.shape[0]},
        {'Klasifikasi': 'Fisik', 'Total': HS_Physical_tweets.shape[0]},
        {'Klasifikasi': 'Gender', 'Total': HS_Gender_tweets.shape[0]},
        {'Klasifikasi': 'Lainnya', 'Total': HS_Other_tweets.shape[0]}
    ]
    data_frame = pd.DataFrame(data)
    return data_frame

def calculateGroupHateSpeech():
    df_group = getDataGroupHateSpeech()
    HS_Religion_tweets = df_group[(df_group['HS_Religion'] ==1)]
    HS_Race_tweets = df_group[(df_group['HS_Race'] ==1)]
    HS_Physical_tweets = df_group[(df_group['HS_Physical'] ==1)]
    HS_Gender_tweets = df_group[(df_group['HS_Gender'] ==1)]
    HS_Other_tweets = df_group[(df_group['HS_Other'] ==1)]
    data = [
        {'Klasifikasi': 'Agama', 'Total': HS_Religion_tweets.shape[0]},
        {'Klasifikasi': 'Ras', 'Total': HS_Race_tweets.shape[0]},
        {'Klasifikasi': 'Fisik', 'Total': HS_Physical_tweets.shape[0]},
        {'Klasifikasi': 'Gender', 'Total': HS_Gender_tweets.shape[0]},
        {'Klasifikasi': 'Lainnya', 'Total': HS_Other_tweets.shape[0]}
    ]
    data_frame = pd.DataFrame(data)
    return data_frame

def calculateClassificationHateSpeech():
    HS_Individual_tweets = df[(df['HS_Individual'] ==1)]
    total_HS_Individual_tweets = HS_Individual_tweets.shape[0]
    HS_Group_tweets = df[(df['HS_Group'] ==1)]
    total_HS_Group_tweets = HS_Group_tweets.shape[0]
    data = [
        {'Tipe': 'Individu', 'Total': total_HS_Individual_tweets, 'Persentase': (total_HS_Individual_tweets / total_HS_tweets) * 100},
        {'Tipe': 'Grup', 'Total': total_HS_Group_tweets, 'Persentase': (total_HS_Group_tweets / total_HS_tweets) * 100}
    ]
    data_frame = pd.DataFrame(data)
    return data_frame

def calculateCharacteristicHateSpeech():
    HS_Weak_tweets = df[(df['HS_Weak'] ==1)]
    total_HS_Weak_tweets = HS_Weak_tweets.shape[0]
    HS_Moderate_tweets = df[(df['HS_Moderate'] ==1)]
    total_HS_Moderate_tweets = HS_Moderate_tweets.shape[0]
    HS_Strong_tweets = df[(df['HS_Strong'] ==1)]
    total_HS_Strong_tweets = HS_Strong_tweets.shape[0]
    data = [
        {'Jenis': 'Lemah', 'Total': total_HS_Weak_tweets, 'Persentase': (total_HS_Weak_tweets / total_HS_tweets) * 100},
        {'Jenis': 'Moderat', 'Total': total_HS_Moderate_tweets, 'Persentase': (total_HS_Moderate_tweets / total_HS_tweets) * 100},
        {'Jenis': 'Kuat', 'Total': total_HS_Strong_tweets, 'Persentase': (total_HS_Strong_tweets / total_HS_tweets) * 100},
    ]
    data_frame = pd.DataFrame(data)
    return data_frame

def calculateNegativeTweetsPercentage():
    HS_tweets = df[(df['HS'] ==1) & (df['Abusive'] ==0)]
    Abusive_tweets = df[(df['HS'] ==0) & (df['Abusive'] ==1)]
    HS_Abusive_tweets = df[(df['HS'] ==1) & (df['Abusive'] ==1)]
    HS_tweets_percentage = (HS_tweets.shape[0] / total_negative_tweets) * 100
    Abusive_tweets_percentage = (Abusive_tweets.shape[0] / total_negative_tweets) * 100
    HS_Abusive_tweets_percentage = (HS_Abusive_tweets.shape[0] / total_negative_tweets) * 100
    data = [
        {'label': 'Hate Speech', 'value': HS_tweets_percentage},
        {'label': 'Abusive', 'value': Abusive_tweets_percentage},
        {'label': 'Hate Speech \nAnd Abusive', 'value': HS_Abusive_tweets_percentage}
    ]
    data = pd.DataFrame(data)
    return data

def calculatePositiveNegativeTweetsPercentage():
    negative_percentage = (total_negative_tweets / total_data) * 100
    positive_percentage = (positive_tweets.shape[0] / total_data) * 100
    data = [
            {'label': 'Positif','value': positive_percentage},
            {'label': 'Negatif', 'value': negative_percentage}
        ]
    data = pd.DataFrame(data)
    return data

def generateBarChart(data: pd.DataFrame, title: str):
    fig, ax = plt.subplots()
    labels = data.iloc[:, 0].tolist()
    values = data.iloc[:, 1].tolist()
    no_of_colors= len(values)
    color= generateRandomColor(no_of_colors)
    ax.bar(labels, values, color=color)
    ax.set_title(title)
    title = title.lower().strip()
    title = re.sub(r"\s+", '-', title)
    title = title + '-bar'
    plt.savefig('./static/images/' + title + '.png')
    fileName = title + '.png'
    fileName = 'images/' + fileName
    return fileName

def generatePieChart(data: pd.DataFrame, title: str):
    matplotlib.use('Agg')
    labels = data.iloc[:, 0].tolist()
    percentage = data.iloc[:, 1].tolist()
    fig1, ax1 = plt.subplots()
    ax1.pie(percentage, labels=labels, wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' }, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    ax1.set_title(title)
    title = title.lower().strip()
    title = re.sub(r"\s+", '-', title)
        # Save the plot to a file
    title = title + '-pie'
    plt.savefig('./static/images/' + title + '.png')
    fileName = title + '.png'
    fileName = 'images/' + fileName
    return fileName

def generateSentimentChart():
    data = calculatePositiveNegativeTweetsPercentage()
    fileName = generatePieChart(data, 'Sentimen Tweet')
    return fileName

def generateNegativeTweetChart():
    data = calculateNegativeTweetsPercentage()
    fileName = generatePieChart(data, 'Tweet Negatif')
    return fileName

def generateCharacteristicHateSpeechPieChart():
    data = calculateCharacteristicHateSpeech()
    fileName = generatePieChart(data, 'Karakteristik Hate Speech')
    return fileName

def generateClassificationHateSpeechBarChart():
    data = calculateClassificationHateSpeech()
    fileName = generateBarChart(data, 'Klasifikasi Hate Speech')
    return fileName, data

def generateCharacteristicHateSpeechBarChart(): 
    data = calculateCharacteristicHateSpeech()
    fileName = generateBarChart(data, 'Karakteristik Hate Speech')
    return fileName, data

def generateIndividualHateSpeeh():
    data = calculateIndividualHateSpeech()
    fileName = generateBarChart(data, 'Hate Speech Individu')
    return fileName, data

def generateGroupHateSpeeh():
    data = calculateGroupHateSpeech()
    fileName = generateBarChart(data, 'Hate Speech Grup')
    return fileName, data