import time
from collections import deque

from nltk.parse.corenlp import CoreNLPParser

f = open("test.txt", "r")
s=f.read()
f.close()
sentences=s.split("\n")

labels={'LS', 'VVP', 'VBD', 'FRAG', 'SENT', 'TO', 'PDT', 'PRP$', 'VVZ', 'VBG', 'NNP', 'NPS', 'WP$', 'SYM', 'POS', 'VH', 'WDT', 'WP', 'RBS', 'VV', 'S', 'MD', 'VVD', 'VBP', 'VHP', 'RB', 'VBZ', 'VVG', 'WRB', 'CC', 'JJS', 'CD', 'VHN', 'NP-TMP', 'UH', 'RBR', 'PP', 'RP', 'ADJP', 'VVN', 'NP', 'VP', 'SBAR', 'PRP', 'NN', 'VB', 'ROOT', 'ADVP', 'VHD', 'VHG', 'FW', 'DT', 'PPZ', 'VHZ', 'VBN', 'EX', 'NNS', 'IN', 'JJR', 'JJ'}

def converter(s):
    ans=""
    i=0
    while(i<len(s)):
        if s[i]=='(':
            j=i+2
            label=""
            while(j<len(s) and s[j]!='\''):
                label+=s[j]
                j+=1
            labels.add(label)
            ans+='['
            i+=1
        elif s[i]==')':
            ans+=']'
            i+=1
        elif s[i]=='"':
            j=i+1
            while s[j]!='"':
                ans+=s[j]
                j+=1
            if(s[j+1]==","):
                ans+=" "
            i=j+1
        elif s[i]=='\'':
            j=i+1
            while s[j]!='\'':
                ans+=s[j]
                j+=1
            if(s[j+1]==","):
                ans+=" "
            i=j+1
        else:
            i+=1
    return ans

#parser = CoreNLPParser(url='http://127.0.0.1:9000')
parser = CoreNLPParser(url='http://localhost:9000')

original=[]
parsed=[]

def parse_square_bracket_notation(s):
    stack1=deque()
    stack2=deque()
    dict={}
    curr_head=''
    prev_head=''
    curr_dict={}
    prev_dict=-1
    i=0
    while(i<len(s)):
        if s[i]=='[':
            j=i+1
            prev_head=curr_head
            curr_head=''
            while(s[j]!=" "):
               curr_head+=s[j]
               j+=1
            stack1.append(curr_head)
            if(prev_dict!=-1):
                curr_dict[prev_head].append({curr_head : []})
                prev_dict=curr_dict
                curr_dict=curr_dict[prev_head][-1]
                stack2.append(curr_dict)
            else:
                dict[curr_head]=[]
                curr_dict=dict
                prev_dict=dict
                stack2.append(curr_dict)
            i=j
        elif s[i]==' ' and s[i+1]!='[':
            j=i+1
            word=''
            while(s[j]!=']'):
                word+=s[j]
                j+=1
            curr_dict[curr_head]=[word]
            i=j
        elif s[i]==']':
            if stack1:
                stack1.pop()
                stack2.pop()
                if stack1:
                    curr_head=stack1[-1]
                    curr_dict=stack2[-1]
            i+=1
        else:
            i+=1
    return dict

f=open('output.txt', 'w')

start_time = time.time()

for i in sentences:
    if i.strip()=='' or i.strip()[0]=='#':
        continue
    temp=i.split(': ')
    parse=str(list(parser.parse(temp[0].split())))
    # output=temp[0]+':'+str(parse_square_bracket_notation(converter(parse)))+':'+str(parse_square_bracket_notation(temp[1]))
    # output=temp[0]+': Obtained: '+converter(parse)+': Expected: '+temp[1]
    output=temp[0]+': Obtained: '+converter(parse)
    if len(temp)!=1:
        original.append(parse_square_bracket_notation(temp[1]))
        parsed.append(parse_square_bracket_notation(converter(parse)))
    f.write(output)
    f.write('\n')

f.close()

print("--- %s seconds ---" % (time.time() - start_time))

print("Output.txt successfully generated")


def calc_exact_score(gold_tree_list, predicted_tree_list):
    total=0
    correct=0
    
    for i in range(len(gold_tree_list)):
        if gold_tree_list[i]==predicted_tree_list[i]:
            correct+=1
        total+=1

    exact_score=correct/total
    return exact_score

def head_finder(s):
    stack=deque()
    stack.append(('ROOT',s['ROOT']))
    visited=[]
    head={}
    while(stack):
        v=stack.pop()
        if v[1] not in visited:
           visited.append(v[1])
        for i in v[1]:
            l=list(i.keys())[0]
            if i[l] in visited:
                continue
            if isinstance(i[l][0],str):
                if i[l][0] in head.keys():
                    head[i[l][0]].append(l)
                    head[i[l][0]].sort()
                else:
                    head[i[l][0]]=[l]
                continue
            else:
                stack.append((l,i[l]))
    return head



def calc_uas(gold_tree_list, predicted_tree_list):
    correct = 0
    total = 0
    for k in range(len(gold_tree_list)):
        goldTree=gold_tree_list[k]
        predictedTree=predicted_tree_list[k]
        head_label_gold=head_finder(goldTree)
        head_label_pred=head_finder(predictedTree)
        for i in head_label_gold.keys():
            n=len(head_label_gold[i])
            total+=n
            for j in range(n):
                if head_label_gold[i][j]==head_label_pred[i][j]:
                    correct+=1
    uas = correct / total
    return uas

def head_label_finder(s):
    stack=deque()
    stack.append(((0,'ROOT'),s['ROOT']))
    visited=[]
    label_head={}
    while(stack):
        v=stack.pop()
        if v[1] not in visited:
           visited.append(v[1])
        for i in v[1]:
            l=list(i.keys())[0]
            if i[l] in visited:
                continue
            if isinstance(i[l][0],str):
                if i[l][0] in label_head.keys():
                    label_head[i[l][0]].append((v[0][1],l))
                    label_head[i[l][0]].sort()
                else:
                    label_head[i[l][0]]=[(v[0][1],l)]
                continue
            stack.append(((v[0][1],l),i[l]))
    return label_head


def calc_las(gold_tree_list, predicted_tree_list):
    correct = 0
    total = 0

    for k in range(len(gold_tree_list)):
        goldTree=gold_tree_list[k]
        predictedTree=predicted_tree_list[k]
        head_label_gold=head_label_finder(goldTree)
        head_label_pred=head_label_finder(predictedTree)
        # print(head_label_gold, head_label_pred)
        for i in head_label_gold.keys():
            n=len(head_label_gold[i])
            total+=n
            for j in range(n):
                if head_label_gold[i][j][1]==head_label_pred[i][j][1] and head_label_gold[i][j][0]==head_label_pred[i][j][0]:
                    correct+=1
    las = correct/total
    return las
# print(original[0], parsed[0])

es=calc_exact_score(original, parsed)
uas=calc_uas(original, parsed)
las=calc_las(original, parsed)

print('Exact Score: ', es)
print('Unlabeled Attachment Score (UAS): ', uas)
print('Labeled Attachment Score (LAS): ', las)
print('Labels are:', labels)
