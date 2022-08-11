
punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
# lists of words to use

positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())

def strip_punctuation(s):
    new_s = ""
    for c in s:
        if c not in punctuation_chars:
            new_s = new_s + c
    return new_s

def get_pos(s_pos):
    pos_w = strip_punctuation(s_pos).lower()
    pos_w = pos_w.split(" ")
    ind_pos = 0
    for w in pos_w:
        if w in positive_words:
            ind_pos = ind_pos + 1
    return ind_pos

def get_neg(s_neg):
    neg_w = strip_punctuation(s_neg).lower()
    neg_w = neg_w.split(" ")
    ind_neg = 0
    for w in neg_w:
        if w in negative_words:
            ind_neg = ind_neg + 1
    return ind_neg

project_twitter = open("project_twitter_data.csv", "r")
c = project_twitter.readlines()


results = open("resulting_data.csv", "w")
results.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score")
results.write("\n")

for line in c[1:]:
    str_item = line.strip().split("\n")
    #print(str_item)
    for word in str_item:
        word = word.split(",")
        #print(word)
        ret = word[1]
        rep = word[2]
        #print(ret)
        #print(rep)
    pos_tweet = 0
    neg_tweet = 0
    pos_tweet = get_pos(line)
    neg_tweet = get_neg(line)
    #print(pos_tweet, ";", neg_tweet)
    net_score = pos_tweet - neg_tweet

    row_string = "{},{},{},{},{}".format(ret, rep, pos_tweet, neg_tweet, net_score)
    results.write(row_string)
    results.write("\n")

close("resulting_data.csv")

