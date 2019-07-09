import math

#scrapin method rank
scraping_rank = open(r"C:\Users\elelo\Desktop\WIR\Top_100.txt", encoding="utf8").read().splitlines()

#Blind method rank
blind_pr = open(r"C:\Users\elelo\Desktop\WIR\blind_PageRank.txt", encoding="utf8").read().splitlines()
blind_rank = [None]*100
for i in range(100):
    blind_rank[i] = blind_pr[i].split("'")[1]


#Rolling Stones rank
RS_rank = open(r"C:\Users\elelo\Desktop\WIR\TheRollingStoneResults.txt", encoding="utf8").read().splitlines()


#Top Tens rank
TT_rank = open(r"C:\Users\elelo\Desktop\WIR\TheTopTensResults.txt", encoding="utf8").read().splitlines()


#Ranker rank
R_rank = open(r"C:\Users\elelo\Desktop\WIR\RankerDotComResults.txt", encoding="utf8").read().splitlines()


def compute_relevance(truth_list, k):
    #<singer: relevance>
    res={}
    for i in range(k):
        #rel of singer in position i = 1/log(i+1+1) base 2
        #log(i+1) is the normal formula, we add another +1
        #because the index i starts from 0 but in the original formula i starts from 1
        res[truth_list[i]]=1/float(math.log(i+1+1, 2))
        
    return res

#compute dcg of list l at k with relevance values in relevance_dict (computed with compute_relvance)
#NB: put suitable value of k!!
def compute_dcg(relevance_dict, l, k):
    res = 0
    for i in range(k):
        if (l[i] in relevance_dict):
            #print(l[i])
            #rel in i-th position / log(i+2) base 2 (same consideration for the +2 as before)
            res = res + relevance_dict[l[i]]/float(math.log(i+2, 2))

    return res

def compute_similarity(relevance_dict, truth_list, our_list, k):
    truth_dcg = compute_dcg(relevance_dict, truth_list, k)
    our_dcg = compute_dcg(relevance_dict, our_list, k)
    res = our_dcg/float(truth_dcg)
    
    return res

###COMPUTE SIMILARITIES
#TT
TT_relevance_dict = compute_relevance(TT_rank, 10)
print("Similarity with respect to thetoptens.com at 10:")
print("For scraping method: ", end="")
print(compute_similarity(TT_relevance_dict, TT_rank, scraping_rank, 10))

print("For blind method: ", end="")
print(compute_similarity(TT_relevance_dict, TT_rank, blind_rank, 10))
print("\n")

#Ranker
R_relevance_dict_30 = compute_relevance(R_rank, 30)
R_relevance_dict_10 = compute_relevance(R_rank, 10)

print("Similarity with respect to Ranker.com:")
print("For scraping method at 30: ", end="")
print(compute_similarity(R_relevance_dict_30, R_rank, scraping_rank, 30))

print("For blind method at 30: ", end="")
print(compute_similarity(R_relevance_dict_30, R_rank, blind_rank, 30))

print("For thetoptens.com at 10: ", end="")
print(compute_similarity(R_relevance_dict_10, R_rank, TT_rank, 10))
print("\n")

#RS
RS_relevance_dict_30 = compute_relevance(RS_rank, 30)
RS_relevance_dict_10 = compute_relevance(RS_rank, 10)

print("Similarity with respect to Rolling Stone:")
print("For scraping method at 30: ", end="")
print(compute_similarity(RS_relevance_dict_30, RS_rank, scraping_rank, 30))

print("For blind method at 30: ", end="")
print(compute_similarity(RS_relevance_dict_30, RS_rank, blind_rank, 30))

print("For Ranker.com at 10: ", end="")
print(compute_similarity(RS_relevance_dict_10, RS_rank, R_rank, 10))
print("For Ranker.com at 30: ", end="")
print(compute_similarity(RS_relevance_dict_30, RS_rank, R_rank, 30))
