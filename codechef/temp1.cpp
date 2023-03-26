#include<iostream>
using namespace std;
long long int addMod(long long x,long long y,int mod){
    return ((x)%mod + (y)%mod)%mod;}
long long int multMod(long long x,long long y,int mod){    return( (x%mod) * (y%mod))%mod;
}bool allowed(int** givenMat,int i,int j,int n){
    bool possible =true;    for(int k=1;k<=j;k++){
        if(givenMat[k][i]==1){            possible=false;
            break;        }
    }    if(possible)
    for(int k=j+1;k<=i;k++){
        if(givenMat[k][i]==2){            possible=false;
            break;        }
    }    return possible;
}long long solve(int** givenMat,int n){
    /vS[i][j] = no of valid strigs of length i and last character different from last index at j    vS[i][0] has all characters equal/
    long long * validSubstrings = new long long[n+1];    for(int i=0;i<n+1;i++){
        validSubstrings[i] = new long long[n+1];    }
    for(int i=0;i<=n;i++){        for(int j=0;j<=n;j++){
            validSubstrings[i][j]=0;        }
    }     validSubstrings[1][0]=2;
    if(givenMat[1][1]==2)        return 0;
    for(int i=2;i<=n;i++){        for(int j=0;j<i;j++){
            if(allowed(givenMat,i,j,n)){                if(j-i+1){
                    validSubstrings[i][j]=(validSubstrings[i-1][j]);                    
                }                else{
                    for(int k=0;k<i-1;k++){                        validSubstrings[i][j]= addMod(validSubstrings[i][j],(validSubstrings[i-1][k]),1000000007 );
                    }                }
            }        }
    }    long long ans = 0;
    for(int i=0;i<n;i++){        ans=addMod(ans,validSubstrings[n][i],1000000007 );
        cout<<validSubstrings[n][i];        cout<<endl;
    }    
    return ans;    
}int main(){
    int n,q;    std::cin>>n>>q;
    int *constraintMatrix = new int[n+1];    for(int i=0;i<n+1;i++){
        constraintMatrix[i] = new int[n+1];    }
    for(int i=0;i<n+1;i++){        for(int j= 0;j<n+1;j++){
            constraintMatrix[i][j] = 0;        }
    }    for(int i= 0;i<q;i++){
        int msg,l,r;        cin>>msg>>l>>r;
        constraintMatrix[l][r] = msg;
    }    
    long long ans =solve(constraintMatrix,n);    std::cout<<ans<<std::endl;
}