# -*- coding: utf-8 -*-
"""B21CS066_Lab_Assignment_8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cuu7Fk4qbDTtRgt9zGzFkXJkRbrxlEiY
"""

!pip install mlxtend
!pip install mlxtend --upgrade --no-deps

"""#Import libraries"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as exp
from sklearn.decomposition import PCA 
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split as tts
from sklearn.model_selection import cross_val_score as CVS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
from sklearn.svm import SVC
from sklearn.metrics import make_scorer
from sklearn.feature_selection import mutual_info_classif



"""#Problem 1

##Part 1
"""

df=pd.read_csv('/content/drive/MyDrive/PRML/LAB-08/train.csv')
df.drop(df.iloc[:,0:1],axis=1,inplace=True)
df

df.info()

df.drop('id',axis=1,inplace=True)
df.dropna(inplace=True)

lab_enc=LabelEncoder()
for header in df.columns:
    if(df[header].dtype=='object'):
        df[header]=lab_enc.fit_transform(df[header])

df

X=df.drop('satisfaction',axis=1)
y=df['satisfaction']

X.isnull().sum()



"""##Part 2"""

dtc_clf=DecisionTreeClassifier()
sfs=SFS(dtc_clf,k_features=10,forward=True,floating=False,scoring='accuracy',cv=4)
sfs.fit(X,y)

sfs.k_score_

sfs.k_feature_names_



"""##Part 3"""

sfs=SFS(dtc_clf,k_features=10,forward=True,floating=False,scoring='accuracy',cv=4)
sfs.fit(X,y)

sbs=SFS(dtc_clf,k_features=10,forward=False,floating=False,scoring='accuracy',cv=4)
sbs.fit(X,y)

sffs=SFS(dtc_clf,k_features=10,forward=True,floating=True,scoring='accuracy',cv=4)
sffs.fit(X,y)

sbfs=SFS(dtc_clf,k_features=10,forward=False,floating=True,scoring='accuracy',cv=4)
sbfs.fit(X,y)

print(f'accuray of sfs is: ',sfs.k_score_)
print(f'accuray of sbs is: ',sbs.k_score_)
print(f'accuray of sffs is: ',sffs.k_score_)
print(f'accuray of sbfs is: ',sbfs.k_score_)



"""##Part 4"""

print('SFS')
pd.DataFrame.from_dict(sfs.get_metric_dict()).T

print('SBS')
pd.DataFrame.from_dict(sbs.get_metric_dict()).T

print('SFFS')
pd.DataFrame.from_dict(sffs.get_metric_dict()).T

print('SBFS')
pd.DataFrame.from_dict(sbfs.get_metric_dict()).T

plot_sfs(sfs.get_metric_dict(), kind='std_dev')
plt.title('SFS')
plt.show()

plot_sfs(sbs.get_metric_dict(), kind='std_dev')
plt.title('SBS')

plot_sfs(sffs.get_metric_dict(), kind='std_dev')
plt.title('SFFS')

plot_sfs(sbfs.get_metric_dict(), kind='std_dev')
plt.title('SBFS')



"""##Part 5"""

#function to get the next feature to push in Sf in sequential forward selection
def Push_next(X,y,Sf,similarity_measure,isGreaterBetter):
    #initializing scores
    best_score=0;
    best_ind=-1; #it denotes feature with maximum similarity score
    worst_score=0;
    worst_ind=-1; #it denotes feature with minimum similarity score

    #iterating over the reamining features to calculate the similarity score for each feature
    for i in range(X.shape[1]):

        #checking if Sf is empty or not. If empty, we cannot apply column stack operation to it
        #if not, we will create a temperory variable which consists of Sf and a new feature whose similarity score we have to find out
        if(Sf.shape==(0,)):
            temp_Sf=X[:,i]
        else:
            temp_Sf=np.c_[Sf,X[:,i]]


        #calculating similarity score
        score=similarity_measure(temp_Sf,y)

        #updating the feature indices with maximum and minimum scores
        if(score>best_score):
            best_score=score
            best_ind=i
        if(score<worst_score):
            worst_score=score
            worst_ind=i

    #checking if isGreaterBetter. This is because in case of accuracy, greater score is better and we should return the feature with best score while in case of distance measures, we should return feature with least similarity score (less the distance, more the accuracy)
    #assigning the next feature (next feat) we are going to add in the Sf
    if(isGreaterBetter):
        next_feat=best_ind
    else:
        next_feat=worst_ind

    
    #adding the next feat to the Sf
    if(Sf.shape==(0,)):
        Sf=X[:,next_feat]
    else:
        Sf=np.c_[Sf,X[:,next_feat]]

    #deleting the selected feature from the whole set of features.
    X=np.delete(X,next_feat,axis=1)
    return X,Sf

    

#function to pull next worst feature from the whole set of features in sequential backward selection algorithm
def Pull_next(X,y,Sb,similarity_measure,isGreaterBetter):
    #initializing scores
    best_score=0;
    best_ind=-1;#it denotes feature which gives us maximum similarity score on removing from the whole set of features
    worst_score=0;
    worst_ind=-1;#it denotes feature which gives us minimum similarity score on removing from the whole set of features

    #iterating over the reamining features to calculate the similarity score for each feature
    for i in range(X.shape[1]):

        #creating a local variable which is consisting of all the features except the feature for which we want to calculate the similarity score
        temp_x=np.delete(X,i,axis=1)

        #calculating the similarity score
        score=similarity_measure(temp_x,y)

        #updating features with maximum and minimum similarity score
        if(score>best_score):
            best_score=score
            best_ind=i
        if(score<worst_score):
            worst_score=score
            worst_ind=i

    
    #similar thing we did in the push_next function. 
    if(isGreaterBetter):
        next_feat=best_ind
    else:
        next_feat=worst_ind

    #updating the Sb set. Adding the removed feature to it
    if(Sb.shape==(0,)):
        Sb=X[:,next_feat]
    else:
        Sb=np.c_[Sb,X[:,next_feat]]

    #Deleting the rejected feature from the whole set of features
    X=np.delete(X,next_feat,axis=1)

    #returning the updated sets
    return X,Sb
            

def Bi_directional_Feature_Set_Generation(X,y,similarity_measure,k_features,isGreaterBetter=1):
    total_features=X.shape[1]
    #initializing the Xf (full set of features for forward selection), Sf (selected features set for forward selection, Xb (full set of features for backward selection) and Sb (removed feature in backwward selection))
    Xf=X.copy()
    Xb=X.copy()
    Sf=np.array([])
    Sb=np.array([])
    
    #no of features stored or removed from the full set of features
    n_features=0

    #this loop will run till either Sf contains k_features or Xb contains k_features
    while(n_features<k_features and (total_features-n_features)>k_features):
        Xf,Sf=Push_next(Xf,y,Sf,similarity_measure,isGreaterBetter) #Pushing next best feature to Sf and removing it from Xf
        Xb,Sb=Push_next(Xb,y,Sb,similarity_measure,isGreaterBetter) #Pulling next worst feature from Xb and pushing it to Sb
        
        n_features+=1
        print('no_of_iteration: ',n_features)
    print(n_features,k_features)

    #if the while loop break because no of features in Sf is equal to k_features, then return Sf. Else, Xb
    if(n_features==k_features):
        return Sf
    else:
        return Xb

def DTC_similarity_measure(X,y):
    DTC_clf=DecisionTreeClassifier()
    if X.ndim==1:
        X=X.reshape(-1,1)
    scores=CVS(DTC_clf,X,y,cv=5)
    return scores.mean()


def SVM_similarity_measure(X,y):
    
    SVM_clf=SVC()
    if X.ndim==1:
        X=X.reshape(-1,1)
    X_train,X_test,y_train,y_test=tts(X,y,train_size=0.1)
    SVM_clf.fit(X_train,y_train)
    return SVM_clf.score(X_test,y_test)

X_red=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),DTC_similarity_measure,10)

pd.DataFrame(X_red,columns=np.arange(X_red.shape[1]))

def find_index(arr,X):
    for i in range(arr.shape[1]):
        if((arr[:,i]==X).all()):
            return i
    return -1

def selected_features_index(arr,X):
    selected_features=[]
    for i in range(X.shape[1]):
        selected_features.append(find_index(arr,X[:,i]))
    selected_features.sort()
    return selected_features

selected_features=selected_features_index(X.to_numpy(),X_red)
print("selected features in bidirectional feature selection through Decision tree classifier accuracy measure are: ",selected_features)

X_red_SVM=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),SVM_similarity_measure,10)
selected_features_SVM=selected_features_index(X.to_numpy(),X_red_SVM)



print("selected features in bidirectional feature selection through SVM classifier accuracy measure are: ",selected_features_SVM)

def Euclidian_distance(x,y):

    temp=x-y
    temp=temp**2
    temp=temp.sum()
    
    temp=np.sqrt(temp)
    return temp

Euclidian_scorer=make_scorer(Euclidian_distance,greater_is_better=False)
def Euclidian_similarity_measure(X,y):
    clf=DecisionTreeClassifier()
    if X.ndim==1:
        X=X.reshape(-1,1)

    scores=CVS(clf,X,y,cv=5,scoring=Euclidian_scorer)
    return scores.mean()

X_red_Euclidian=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),Euclidian_similarity_measure,10)
selected_features_Euclidian=selected_features_index(X.to_numpy(),X_red_Euclidian)



print("selected features in bidirectional feature selection through Decision tree classifier and Euclidian Distance measure are: ",selected_features_Euclidian)

print(Euclidian_scorer(DecisionTreeClassifier().fit(X[:1000],y[:1000]),X,y))
print(Euclidian_distance(DecisionTreeClassifier().fit(X[:1000],y[:1000]).predict(X),y))

def City_block_distance(x,y):
    temp=x-y
    temp=np.abs(temp)
    temp=temp.sum()
    return temp

City_block_scorer=make_scorer(City_block_distance,greater_is_better=False)
def City_block_similarity_metric(X,y):
    clf=DecisionTreeClassifier()
    if X.ndim==1:
        X=X.reshape(-1,1)
    scores=CVS(clf,X,y,cv=5,scoring=City_block_scorer)
    return scores.mean() 

X_red_City_block=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),City_block_similarity_metric,10)
selected_features_City_block=selected_features_index(X.to_numpy(),X_red_City_block)

print("selected features in bidirectional feature selection through Decision tree classifier and City block Distance measure are: ",selected_features_City_block)

def Angular_distance(x,y):
    
    dot_product = np.sum(x * y)
    norm1 = np.linalg.norm(x)
    norm2 = np.linalg.norm(y)
    angular_distance = dot_product / (norm1 * norm2)
    
    return angular_distance

Angular_scorer=make_scorer(Angular_distance,greater_is_better=False)
def Angular_similarity_metric(X,y):
    clf=DecisionTreeClassifier()
    if X.ndim==1:
        X=X.reshape(-1,1)
    scores=CVS(clf,X,y,cv=5,scoring=Angular_scorer)
    return scores.mean() 

X_red_Angular=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),Angular_similarity_metric,10)
selected_features_Angular=selected_features_index(X.to_numpy(),X_red_Angular)

print("selected features in bidirectional feature selection through Decision tree classifier and Euclidian Distance measure are: ",selected_features_Angular)

# X_red_SVM=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),SVM_similarity_measure,10)

Angular_distance(np.array([1,1,1,1]),np.array([1,1,1,1]))

def info_gain_similarity_measure(X,y):
    if(X.ndim==1):
        X=X.reshape(-1,1)
    return mutual_info_classif(X,y).sum()

X_red_info_gain=Bi_directional_Feature_Set_Generation(X.to_numpy(),y.to_numpy(),info_gain_similarity_measure,10)
selected_features_info_gain=selected_features_index(X.to_numpy(),X_red_info_gain)

print("selected features in bidirectional feature selection through Information gain are: ",selected_features_info_gain)

for X,similarity_measure in zip([X_red,X_red_SVM,X_red_info_gain,X_red_Euclidian,X_red_City_block,X_red_Angular],['Decision tree accuracy measure','SVM classifier accuracy measure','Information gain','Euclidian distance measure','City block measure','Angular distance measure']):
    clf=DecisionTreeClassifier()
    scores=CVS(clf,X,y,cv=5)
    print(similarity_measure,':',scores.mean())

"""#Problem 2

##Part 1
"""

mean=np.zeros(3,dtype=int)
cov=np.array([[0.6006771,0.14889879,0.244939],[0.14889879,0.58982531,0.24154981],[0.244939,0.24154981,0.48778655]])
# mean
X=np.random.multivariate_normal(mean,cov,size=1000)
X

r_6=np.sqrt(6)
v=np.array([[1/r_6],[1/r_6],[(-2)/r_6]])
y=np.zeros(X.shape[0],dtype=int)
for i in range(X.shape[0]):
    if(np.dot(X[i,:],v)<=0):
        y[i]=1
y

fig=exp.scatter_3d(X,x=X[:,0],y=X[:,1],z=X[:,2],color=y)
fig.show()

"""##Part 2"""

pca=PCA(n_components=3)
pca.fit(X)
X_red=pca.transform(X)
X_red

"""##Part 3"""

def plot_decision_boundary(clf,X,Y,classes,plot_colors):
    # print(n)
    # new_clf_RFC=  BaggingClassifier(base_estimator=SVC(),n_estimators=n ).fit(X_train,Y_train)
    # print(new_clf_RFC.score(X_test,Y_test))
    
    n_classes = len(classes)
    
    plot_step = 0.04
    


    # X=self.transform(X)
        
        

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                        np.arange(y_min, y_max, plot_step))
    plt.tight_layout(h_pad=0.5, w_pad=0.5, pad=2.5)

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    cs = plt.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu)

    plt.xlabel("X1")
    plt.ylabel("X2")

    # Plot the training points
    for i, color in zip(range(n_classes), plot_colors):
        idx = np.where(Y == classes[i])
        plt.scatter(X[idx, 0], X[idx, 1], c=color, label=i,
                    cmap=plt.cm.RdYlBu, edgecolor='black', s=16)


    plt.legend(loc='lower right', borderpad=0, handletextpad=0)
    plt.axis("tight")


    plt.show()

dtc_clf=DecisionTreeClassifier()
for features in [[0,1],[1,2],[0,2]]:
    new_X=X_red[:,features]
    X_train,X_test,y_train,y_test=tts(new_X,y,test_size=0.3)
    dtc_clf.fit(X_train,y_train)
    accuracy=dtc_clf.score(X_test,y_test)
    print(f'for {features}')
    print('accuracy: ',accuracy)
    plot_decision_boundary(dtc_clf,X_test,y_test,np.array([0,1]),'rb')

"""##Part 4"""

pca=PCA(n_components=2)
pca.fit(X)
X_red_2=pca.transform(X)
X_red_2

for features in [[0,1],[1,2],[0,2]]:
    print(features)
    temp = X_red[:,features] - X_red_2
    distance = np.sqrt(np.sum(np.square(temp)))
    print(distance,'\n')

"""Here we can see that the euclidian distance between the matrices is least when first two features are selected. So, we can say that when we will apply the pca for 2 components we will get first two features of the dataset that we got from pca for 3 components"""

dtc_clf=DecisionTreeClassifier()
X_train,X_test,y_train,y_test=tts(X_red_2,y,test_size=0.3)
dtc_clf.fit(X_train,y_train)
print(dtc_clf.score(X_test,y_test))
plot_decision_boundary(dtc_clf,X_test,y_test,[0,1],'rb')

for features in [[0,1],[1,2],[0,2]]:
    plot_x=X[:,features[0]]
    plot_y=X[:,features[1]]
    for class_no in np.unique(y):
        idx=np.where(y==class_no)[0]
        plt.scatter(plot_x[idx],plot_y[idx],label=class_no)
    plt.legend(bbox_to_anchor=(1.1, 1.05))
    plt.show()

"""As we can see that first two features are not seperating data effectively in comparision to other two pairs. Therefore, we are getting much less accuracy when we consider first two features to train the model"""

np.cov(X_red,rowvar=False)

"""From here we can see that the standard deviation is higher for first two features therefore pca is giving more weightage to these two features. But this fact is independent of whether the two classes are seperable or not"""

