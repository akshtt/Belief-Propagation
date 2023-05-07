import math
import re
import decimal
decimal.getcontext().prec = 100
def convolve(dict1, dict2):
    result_dict = {}
    sum=0;
    for key1 in dict1:
        for key2 in dict2:
            if(key1+key2 in result_dict):
                result_dict[key1 + key2]+=decimal.Decimal(dict1[key1])*decimal.Decimal(dict2[key2])
            else:
                result_dict[key1 + key2] = decimal.Decimal(dict1[key1])*decimal.Decimal(dict2[key2])
    # for k in result_dict:
    #     sum+=result_dict[k]

    sorted_dict=dict(sorted(result_dict.items()))
    return sorted_dict
def coeff_change(dict1,a):
    newdict={}
    for i in dict1:
        newdict[a*i]=dict1[i]
    sorted_dict=dict(sorted(newdict.items()))
    return sorted_dict
    # return newdict

def distribution_f(dict1):
    sum=0
    df={}
    for i in dict1:
        sum+=dict1[i]
        df[i]=sum
    # print(sum)
    return df
def search_less(arr,x):
    hi=len(arr)-1
    lo=0
    res=-1
    # print(hi)
    # print(lo)
    while(lo<=hi):

        m=math.floor((hi+lo)/2)
        # print(m)
        if(arr[m]<x):
            res=m
            lo=m+1
        else:
            hi=m-1
    
    return res

def prob_less(dict1, x):
    key=dict1.keys()
    key=list(key)
    ind=search_less(key,x)
    if(ind==-1) : return 0
    return dict1[key[ind]]
def prob_more(dict1, x):
    key=dict1.keys()
    key=list(key)
    ind=search_less(key,x)
    if(ind==-1) : return 1
    return 1-dict1[key[ind]]

def msg_for_variables_less(dict1, dict2, b,a):
    # print(a)

    dict2=distribution_f(dict2)
    sum=0
    for i in dict1:
        ans=prob_less(dict2,b-a*i)
        dict1[i]=ans
        sum+=dict1[i]
    if sum!=0:
        for i in dict1:
            dict1[i]/=sum
    return dict1
def msg_for_variables_grt(dict1,dict2,b,a):
   
    dict2=distribution_f(dict2)
   

    sum=0
    # print(list(dict2.keys()))
    for i in dict1:
       dict1[i]=prob_more(dict2,b-a*i)
       sum+=dict1[i]

    if sum!=0:
        for i in dict1:
            dict1[i]/=sum
    return dict1 
def multiconvolve(a,rem,prior):
    newdict={0:1}
    for i in rem:
        curr=prior[i]
        curr=coeff_change(curr,a[i])
        newdict=convolve(newdict,curr)
    

    # print(newdict)
    return newdict


def msg_from_jnode_to_ivariable(A,B,eq,i,j,prior):
    Aj=A[j]
    bj=B[j]
    s=eq[j]
    rem=list(range(len(A[0])))
    rem.remove(i)
    # print(rem)
    X=prior[i]
    # print(X)
    Y=multiconvolve(Aj,rem,prior) 
    # print(A[j][i])
    if(s==">="):
        return msg_for_variables_grt(X,Y,bj,A[j][i])
    else:
        return msg_for_variables_less(X,Y,bj,A[j][i])
def msg_from_ivariable_to_jnode(i,j,curm):
    newm={}
    sum=0
  

    for k in range(len(curm)):
        if(j==k): continue
        for val in curm[k]:
            if(val in newm):
                newm[val]=decimal.Decimal(curm[k][val])*decimal.Decimal(newm[val])
            else:
                newm[val]=curm[k][val]

   
    for k in newm:
        sum+=newm[k]
        # print(sum)
    # print(newm)
    if(sum!=0):
        for k in newm:
            newm[k]/=sum
    # print(newm)
    newm=dict(sorted(newm.items()))
    return newm

def marginal_of_i(curm):
    newm={}
    sum=0
  

    for k in range(len(curm)):
        for val in curm[k]:
            if(val in newm):
                newm[val]=decimal.Decimal(curm[k][val])*decimal.Decimal(newm[val])
            else:
                newm[val]=curm[k][val]

   
    for k in newm:
        sum+=newm[k]
        # print(sum)
    # print(newm)
    if(sum!=0):
        for k in newm:
            newm[k]/=sum
    # print(newm)
    newm=dict(sorted(newm.items()))
    return newm

def msgs_from_factorj(A,B,eq,j,prior):
    curm=[]
    for i in range(len(A[0])):
        curm.append(msg_from_jnode_to_ivariable(A,B,eq,i,j,prior))
    return curm

def msg_collection_from_factor(A,B,eq,prior_overall):
    newm=[[] for i in range(len(A[0]))]
    for j in range(len(A)):
        c=msgs_from_factorj(A,B,eq,j,prior_overall[j])
        for i in range(len(c)):
            newm[i].append(c[i])
    return newm
def new_prior_calculation(A,x):
    new_prior=[[] for i in range(len(A))]
    for i in range(len(A[0])):
        for j in range(len(A)):
            n=msg_from_ivariable_to_jnode(i,j,x[i])
            new_prior[j].append(n)

    return new_prior   
def marginal(A,x):
    md=[]
    for i in range(len(A[0])):
        md.append(marginal_of_i(x[i]))
    return md

def main():
    
    str='''(0) s0 +	(2) s1 +	(-1) s2 +	(2) s3 +	(-2) s4 +	(3) s5 +	(-1) s6 +	(1) s7 +	26 >= 0
(-3) s0 +	(0) s1 +	(2) s2 +	(-4) s3 +	(-2) s4 +	(-1) s5 +	(1) s6 +	(-1) s7 +	-2 >= 0
(-4) s0 +	(-3) s1 +	(-2) s2 +	(3) s3 +	(-4) s4 +	(2) s5 +	(2) s6 +	(4) s7 +	0 < 0
(-1) s0 +	(-3) s1 +	(1) s2 +	(-3) s3 +	(0) s4 +	(1) s5 +	(0) s6 +	(3) s7 +	52 >= 0
(-1) s0 +	(-3) s1 +	(-4) s2 +	(1) s3 +	(-1) s4 +	(4) s5 +	(0) s6 +	(4) s7 +	70 >= 0
(3) s0 +	(-3) s1 +	(3) s2 +	(-3) s3 +	(0) s4 +	(-3) s5 +	(0) s6 +	(-3) s7 +	-26 < 0
(0) s0 +	(3) s1 +	(2) s2 +	(-3) s3 +	(-1) s4 +	(-1) s5 +	(3) s6 +	(-3) s7 +	-18 < 0
(2) s0 +	(-1) s1 +	(-1) s2 +	(0) s3 +	(0) s4 +	(1) s5 +	(1) s6 +	(4) s7 +	-49 < 0
(0) s0 +	(1) s1 +	(-4) s2 +	(2) s3 +	(-1) s4 +	(-2) s5 +	(1) s6 +	(-3) s7 +	-67 < 0
(1) s0 +	(1) s1 +	(-1) s2 +	(1) s3 +	(-4) s4 +	(-3) s5 +	(-2) s6 +	(-3) s7 +	-22 < 0
(-1) s0 +	(1) s1 +	(0) s2 +	(-2) s3 +	(-1) s4 +	(4) s5 +	(0) s6 +	(-1) s7 +	-29 < 0
(0) s0 +	(-2) s1 +	(1) s2 +	(-2) s3 +	(-3) s4 +	(0) s5 +	(0) s6 +	(4) s7 +	2 >= 0
(-3) s0 +	(-1) s1 +	(1) s2 +	(2) s3 +	(3) s4 +	(-4) s5 +	(3) s6 +	(3) s7 +	-23 < 0
(0) s0 +	(3) s1 +	(3) s2 +	(-2) s3 +	(-1) s4 +	(1) s5 +	(0) s6 +	(-2) s7 +	51 >= 0
(-3) s0 +	(0) s1 +	(-3) s2 +	(1) s3 +	(2) s4 +	(3) s5 +	(0) s6 +	(0) s7 +	-69 < 0
(-4) s0 +	(2) s1 +	(3) s2 +	(2) s3 +	(1) s4 +	(3) s5 +	(0) s6 +	(-3) s7 +	-88 < 0
(1) s0 +	(3) s1 +	(3) s2 +	(3) s3 +	(-3) s4 +	(-2) s5 +	(-1) s6 +	(0) s7 +	-30 < 0
(0) s0 +	(3) s1 +	(0) s2 +	(2) s3 +	(3) s4 +	(0) s5 +	(1) s6 +	(3) s7 +	-17 < 0
(-4) s0 +	(-3) s1 +	(-4) s2 +	(-1) s3 +	(-3) s4 +	(4) s5 +	(-1) s6 +	(-2) s7 +	18 >= 0
(-3) s0 +	(-1) s1 +	(0) s2 +	(3) s3 +	(-4) s4 +	(-4) s5 +	(3) s6 +	(4) s7 +	-38 < 0
(-4) s0 +	(-4) s1 +	(-2) s2 +	(3) s3 +	(1) s4 +	(0) s5 +	(-1) s6 +	(3) s7 +	-9 < 0
(2) s0 +	(-3) s1 +	(2) s2 +	(0) s3 +	(-3) s4 +	(-3) s5 +	(-1) s6 +	(4) s7 +	11 >= 0
(0) s0 +	(2) s1 +	(2) s2 +	(0) s3 +	(4) s4 +	(4) s5 +	(-2) s6 +	(2) s7 +	14 >= 0
(2) s0 +	(-2) s1 +	(2) s2 +	(2) s3 +	(0) s4 +	(1) s5 +	(-4) s6 +	(-1) s7 +	8 >= 0
(0) s0 +	(3) s1 +	(0) s2 +	(2) s3 +	(3) s4 +	(0) s5 +	(1) s6 +	(3) s7 +	-17 < 0
(-1) s0 +	(-1) s1 +	(-2) s2 +	(1) s3 +	(-4) s4 +	(-3) s5 +	(3) s6 +	(1) s7 +	-36 < 0
(3) s0 +	(2) s1 +	(-2) s2 +	(2) s3 +	(2) s4 +	(-2) s5 +	(3) s6 +	(0) s7 +	70 >= 0
(0) s0 +	(0) s1 +	(3) s2 +	(-1) s3 +	(-3) s4 +	(-3) s5 +	(4) s6 +	(2) s7 +	-41 < 0
(-3) s0 +	(-3) s1 +	(-4) s2 +	(-3) s3 +	(-1) s4 +	(-1) s5 +	(-4) s6 +	(-1) s7 +	84 >= 0
(2) s0 +	(-2) s1 +	(1) s2 +	(-4) s3 +	(2) s4 +	(3) s5 +	(-3) s6 +	(-1) s7 +	-78 < 0
(-2) s0 +	(-2) s1 +	(0) s2 +	(-4) s3 +	(3) s4 +	(1) s5 +	(1) s6 +	(-3) s7 +	-6 >= 0
(2) s0 +	(4) s1 +	(4) s2 +	(-2) s3 +	(2) s4 +	(1) s5 +	(4) s6 +	(1) s7 +	-2 < 0
(-1) s0 +	(2) s1 +	(-2) s2 +	(-3) s3 +	(3) s4 +	(0) s5 +	(4) s6 +	(3) s7 +	-3 < 0
(-4) s0 +	(-4) s1 +	(-1) s2 +	(2) s3 +	(-3) s4 +	(-3) s5 +	(0) s6 +	(3) s7 +	-38 < 0
(3) s0 +	(2) s1 +	(-2) s2 +	(2) s3 +	(2) s4 +	(-2) s5 +	(3) s6 +	(0) s7 +	70 >= 0
(-2) s0 +	(1) s1 +	(-1) s2 +	(1) s3 +	(3) s4 +	(0) s5 +	(4) s6 +	(4) s7 +	6 >= 0
(-3) s0 +	(0) s1 +	(-3) s2 +	(1) s3 +	(2) s4 +	(3) s5 +	(0) s6 +	(0) s7 +	-69 < 0
(-2) s0 +	(1) s1 +	(3) s2 +	(-2) s3 +	(3) s4 +	(3) s5 +	(0) s6 +	(-2) s7 +	83 >= 0
(0) s0 +	(1) s1 +	(-4) s2 +	(2) s3 +	(-1) s4 +	(-2) s5 +	(1) s6 +	(-3) s7 +	-67 < 0
(-4) s0 +	(2) s1 +	(-1) s2 +	(-1) s3 +	(1) s4 +	(-2) s5 +	(-4) s6 +	(-1) s7 +	-11 < 0
(1) s0 +	(-1) s1 +	(3) s2 +	(1) s3 +	(0) s4 +	(-2) s5 +	(0) s6 +	(-4) s7 +	-6 < 0
(-4) s0 +	(0) s1 +	(1) s2 +	(2) s3 +	(3) s4 +	(-3) s5 +	(-2) s6 +	(-1) s7 +	92 >= 0
(-2) s0 +	(-1) s1 +	(3) s2 +	(-1) s3 +	(-1) s4 +	(3) s5 +	(-2) s6 +	(-3) s7 +	60 >= 0
(-2) s0 +	(2) s1 +	(-4) s2 +	(1) s3 +	(-3) s4 +	(1) s5 +	(3) s6 +	(4) s7 +	-9 < 0
(-2) s0 +	(0) s1 +	(2) s2 +	(-3) s3 +	(0) s4 +	(-1) s5 +	(0) s6 +	(-4) s7 +	5 >= 0
(0) s0 +	(-3) s1 +	(1) s2 +	(-2) s3 +	(3) s4 +	(3) s5 +	(-2) s6 +	(0) s7 +	-63 < 0
(-2) s0 +	(-4) s1 +	(-1) s2 +	(3) s3 +	(-3) s4 +	(-1) s5 +	(0) s6 +	(4) s7 +	-43 < 0
(-4) s0 +	(0) s1 +	(1) s2 +	(-1) s3 +	(-3) s4 +	(3) s5 +	(2) s6 +	(0) s7 +	-13 < 0
(-4) s0 +	(2) s1 +	(3) s2 +	(2) s3 +	(1) s4 +	(-2) s5 +	(2) s6 +	(2) s7 +	-22 < 0
(1) s0 +	(-3) s1 +	(2) s2 +	(-2) s3 +	(-1) s4 +	(3) s5 +	(0) s6 +	(-2) s7 +	-49 < 0
(2) s0 +	(-3) s1 +	(-3) s2 +	(-1) s3 +	(1) s4 +	(1) s5 +	(-2) s6 +	(3) s7 +	-62 < 0
(-4) s0 +	(-3) s1 +	(-2) s2 +	(-3) s3 +	(3) s4 +	(0) s5 +	(3) s6 +	(2) s7 +	12 >= 0
(2) s0 +	(-1) s1 +	(-4) s2 +	(-1) s3 +	(1) s4 +	(4) s5 +	(-1) s6 +	(4) s7 +	-10 < 0
(-2) s0 +	(0) s1 +	(0) s2 +	(-1) s3 +	(2) s4 +	(3) s5 +	(4) s6 +	(0) s7 +	11 >= 0
(0) s0 +	(-1) s1 +	(2) s2 +	(-2) s3 +	(2) s4 +	(4) s5 +	(-2) s6 +	(-3) s7 +	-53 < 0
(0) s0 +	(3) s1 +	(2) s2 +	(-3) s3 +	(-1) s4 +	(-1) s5 +	(3) s6 +	(-3) s7 +	-18 < 0
(-3) s0 +	(-3) s1 +	(-1) s2 +	(2) s3 +	(2) s4 +	(0) s5 +	(4) s6 +	(1) s7 +	-69 < 0
(1) s0 +	(3) s1 +	(3) s2 +	(0) s3 +	(0) s4 +	(2) s5 +	(4) s6 +	(-1) s7 +	-47 < 0
(3) s0 +	(1) s1 +	(1) s2 +	(-1) s3 +	(2) s4 +	(0) s5 +	(2) s6 +	(-2) s7 +	-26 < 0
(-3) s0 +	(0) s1 +	(2) s2 +	(3) s3 +	(2) s4 +	(0) s5 +	(3) s6 +	(3) s7 +	11 >= 0
(1) s0 +	(0) s1 +	(2) s2 +	(-3) s3 +	(-3) s4 +	(4) s5 +	(2) s6 +	(-1) s7 +	21 >= 0
(-2) s0 +	(-2) s1 +	(0) s2 +	(-4) s3 +	(3) s4 +	(1) s5 +	(1) s6 +	(-3) s7 +	-6 >= 0
(0) s0 +	(3) s1 +	(2) s2 +	(-3) s3 +	(-1) s4 +	(-1) s5 +	(3) s6 +	(-3) s7 +	-18 < 0
(1) s0 +	(2) s1 +	(-2) s2 +	(-4) s3 +	(-1) s4 +	(-3) s5 +	(2) s6 +	(-3) s7 +	-16 < 0
(2) s0 +	(-3) s1 +	(1) s2 +	(1) s3 +	(3) s4 +	(2) s5 +	(2) s6 +	(-2) s7 +	42 >= 0
(-3) s0 +	(-3) s1 +	(-4) s2 +	(-3) s3 +	(-1) s4 +	(-1) s5 +	(-4) s6 +	(-1) s7 +	84 >= 0
(-3) s0 +	(1) s1 +	(-4) s2 +	(0) s3 +	(-3) s4 +	(-1) s5 +	(4) s6 +	(4) s7 +	-3 < 0
(3) s0 +	(2) s1 +	(-1) s2 +	(2) s3 +	(-1) s4 +	(0) s5 +	(1) s6 +	(2) s7 +	-2 < 0
(-2) s0 +	(0) s1 +	(-4) s2 +	(1) s3 +	(-1) s4 +	(-3) s5 +	(3) s6 +	(2) s7 +	-13 < 0
(3) s0 +	(-1) s1 +	(-1) s2 +	(-1) s3 +	(-3) s4 +	(4) s5 +	(3) s6 +	(-2) s7 +	-28 < 0
(2) s0 +	(-4) s1 +	(3) s2 +	(-4) s3 +	(-4) s4 +	(3) s5 +	(1) s6 +	(3) s7 +	-64 < 0
(3) s0 +	(3) s1 +	(2) s2 +	(-3) s3 +	(4) s4 +	(-1) s5 +	(-1) s6 +	(1) s7 +	-24 < 0
(-2) s0 +	(2) s1 +	(-4) s2 +	(1) s3 +	(-3) s4 +	(1) s5 +	(3) s6 +	(4) s7 +	-9 < 0
(0) s0 +	(-3) s1 +	(-3) s2 +	(-3) s3 +	(2) s4 +	(4) s5 +	(-1) s6 +	(-2) s7 +	-34 < 0
(-2) s0 +	(0) s1 +	(-4) s2 +	(1) s3 +	(-1) s4 +	(-3) s5 +	(3) s6 +	(2) s7 +	-13 < 0
(2) s0 +	(-3) s1 +	(0) s2 +	(-2) s3 +	(-1) s4 +	(-1) s5 +	(-1) s6 +	(0) s7 +	1 >= 0
(-2) s0 +	(0) s1 +	(-1) s2 +	(2) s3 +	(-1) s4 +	(2) s5 +	(0) s6 +	(4) s7 +	-42 < 0
(1) s0 +	(1) s1 +	(-1) s2 +	(1) s3 +	(-4) s4 +	(-3) s5 +	(-2) s6 +	(-3) s7 +	-22 < 0
(-4) s0 +	(3) s1 +	(3) s2 +	(-4) s3 +	(3) s4 +	(-3) s5 +	(4) s6 +	(-2) s7 +	-27 < 0
(1) s0 +	(0) s1 +	(-2) s2 +	(-3) s3 +	(-1) s4 +	(0) s5 +	(2) s6 +	(-1) s7 +	-17 < 0
(-2) s0 +	(0) s1 +	(-4) s2 +	(1) s3 +	(-1) s4 +	(-3) s5 +	(3) s6 +	(2) s7 +	-13 < 0
(-2) s0 +	(-1) s1 +	(3) s2 +	(-1) s3 +	(-1) s4 +	(3) s5 +	(-2) s6 +	(-3) s7 +	60 >= 0
(-3) s0 +	(-1) s1 +	(0) s2 +	(3) s3 +	(-4) s4 +	(-4) s5 +	(3) s6 +	(4) s7 +	-38 < 0
(1) s0 +	(0) s1 +	(-2) s2 +	(-3) s3 +	(-1) s4 +	(0) s5 +	(2) s6 +	(-1) s7 +	-17 < 0
(2) s0 +	(-4) s1 +	(0) s2 +	(-4) s3 +	(0) s4 +	(-1) s5 +	(0) s6 +	(1) s7 +	14 >= 0
(2) s0 +	(3) s1 +	(-1) s2 +	(1) s3 +	(-2) s4 +	(2) s5 +	(-3) s6 +	(0) s7 +	-14 < 0
(0) s0 +	(-2) s1 +	(1) s2 +	(-2) s3 +	(-3) s4 +	(0) s5 +	(0) s6 +	(4) s7 +	2 >= 0
(-2) s0 +	(-3) s1 +	(2) s2 +	(2) s3 +	(-2) s4 +	(3) s5 +	(2) s6 +	(0) s7 +	-21 < 0
(-4) s0 +	(0) s1 +	(-3) s2 +	(1) s3 +	(3) s4 +	(3) s5 +	(0) s6 +	(2) s7 +	65 >= 0
(2) s0 +	(-1) s1 +	(-4) s2 +	(-1) s3 +	(1) s4 +	(4) s5 +	(-1) s6 +	(4) s7 +	-10 < 0
(-3) s0 +	(-2) s1 +	(-3) s2 +	(-2) s3 +	(-2) s4 +	(-1) s5 +	(-2) s6 +	(1) s7 +	24 >= 0
(1) s0 +	(2) s1 +	(0) s2 +	(2) s3 +	(3) s4 +	(-3) s5 +	(0) s6 +	(-1) s7 +	-82 < 0
(1) s0 +	(3) s1 +	(3) s2 +	(0) s3 +	(0) s4 +	(2) s5 +	(4) s6 +	(-1) s7 +	-47 < 0
(2) s0 +	(-4) s1 +	(3) s2 +	(-4) s3 +	(-4) s4 +	(3) s5 +	(1) s6 +	(3) s7 +	-64 < 0
(-1) s0 +	(-4) s1 +	(-3) s2 +	(0) s3 +	(-2) s4 +	(-3) s5 +	(0) s6 +	(3) s7 +	-12 < 0
(1) s0 +	(-3) s1 +	(2) s2 +	(-2) s3 +	(-1) s4 +	(3) s5 +	(0) s6 +	(-2) s7 +	-49 < 0
(2) s0 +	(-3) s1 +	(2) s2 +	(1) s3 +	(-1) s4 +	(1) s5 +	(3) s6 +	(-3) s7 +	22 >= 0
(-4) s0 +	(-4) s1 +	(3) s2 +	(-1) s3 +	(1) s4 +	(-3) s5 +	(2) s6 +	(2) s7 +	17 >= 0
(-2) s0 +	(-2) s1 +	(0) s2 +	(-4) s3 +	(3) s4 +	(1) s5 +	(1) s6 +	(-3) s7 +	-6 >= 0
(-3) s0 +	(1) s1 +	(-4) s2 +	(0) s3 +	(-3) s4 +	(-1) s5 +	(4) s6 +	(4) s7 +	-3 < 0'''

# Solution = (s0, s1, s2, s3, s4, s5, s6, s7) = (-1, -1, 1, -1, 1, 0, -1, -1)


    inequalities = str.strip().split('\n')
    regex = r'\(([+-]?\d+)\)\s*(\w\d+)'
    A=[]
    B=[]
    eq=[]
    for inequality in inequalities:
        match = re.findall(regex, inequality)
        inequality_coeffs = [int(m[0]) for m in match]
        inequality_constants = int(re.findall(r'([+-]?\d+)\s*(>=|<=|<|>)', inequality)[0][0])
        inequality_sign = re.findall(r'([+-]?\d+)\s*(>=|<=|<|>)', inequality)[0][1]
        A.append(inequality_coeffs)
        B.append(inequality_constants)
        eq.append(inequality_sign)

    
    # print(A)
    # print(B)
    # print(eq)
    for i in range(len(B)):
        B[i]=-1*B[i]
    
    prior=[]
    for i in range(len(A)):
        g=[]
        for j in range(len(A[0])):
            g.append({-3:decimal.Decimal(1/64),-2:decimal.Decimal(3/32),-1:decimal.Decimal(15/64),0:decimal.Decimal(20/64),1:decimal.Decimal(15/64),2:decimal.Decimal(3/32),3:decimal.Decimal(1/64)})
        prior.append(g)
        # prior.append([{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64}])
    # 1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64},{-3:1/64,-2:3/32,-1:15/64,0:20/64,1:15/64,2:3/32,3:1/64}]]
    # print(msg_from_jnode_to_ivariable(A,B,eq,0,0,prior[0]))
    # print(msgs_from_factorj(A,B,eq,1,prior[1]))

    # print(msg_from_jnode_to_ivariable(A,B,eq,0,0,prior[0]))
    for i in range(1):
        newm=msg_collection_from_factor(A,B,eq,prior)
        # print(newm)
        prior=new_prior_calculation(A,newm)
    # print(newm)
    # print(prior)
   
    sol=[]
    abc=marginal(A,newm)
    # print(prior[0][0])
    for i in range(8):
        sol.append(max(abc[i], key=abc[i].get))
    print(sol)
#     # sol=[1, 1, -1, -2, 0, 2, 1, 1]
#     # # print(abc)
    r = [sum(a*b for a,b in zip(row, sol)) for row in A]
#     # print(distribution_f((multiconvolve(A[19],[0,1,2,3,4,5,6],prior[19]))))
#     # curm=[]

#     # curm.append(msg_from_jnode_to_ivariable(A,B,eq,7,19,prior[19]))
#     # curm.append(msg_from_jnode_to_ivariable(A,B,eq,7,18,prior[18]))
#     # curm.append(msg_from_jnode_to_ivariable(A,B,eq,7,17,prior[17]))
#     # curm.append(msg_from_jnode_to_ivariable(A,B,eq,7,16,prior[16]))
#     # print(marginal_of_i(curm))

# print the result
    cnt=0
    for i in range(len(A)):
      print(f"{r[i]} {eq[i]} {B[i]}")
      if(eq[i]==">="):
        if(r[i]<B[i]):
            print("false")
            cnt+=1
            # break
      else:
        if(r[i]>=B[i]):
            print("false")
            cnt+=1
            # break
    print(cnt)
    
    # print(msg_from_ivariable_to_jnode(0,0,newm[i]))
    # print(msg_from_jnode_to_ivariable(A,B,eq,0,1,prior[1]))

    
main()

